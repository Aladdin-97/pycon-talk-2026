from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django_q.tasks import async_task
from email_templates.models import EmailTemplate
from booking.models import Booking
from app_core.models import Setting
from datetime import datetime, timedelta

import logging

log = logging.getLogger(f"{settings.APP_LOGGER}.{__name__}")
ERR_TEMPLATE = "An exception of type {0} occurred. Arguments:\n{1!r}"
EMAIL_TEMPLATE_NAME = "Post Booking Mail"


def sync_send_booking_mail(booking_obj, user_email):
    log.info(f"Sending booking email synchronously for the user: {user_email}")
    mail_context = dict(
        user=booking_obj.user,
        office=booking_obj.office,
        room=booking_obj.room,
        desk=booking_obj.desk,
        date=booking_obj.booked_on,
        MYBOOK_URL=settings.MYBOOK_URL,
    )
    email_message = get_email_message(mail_context)
    subject = email_message.get("subject")
    message = email_message.get("message")
    html_message = email_message.get("html_message")
    sender = email_message.get("sender")

    try:
        send_mail(
            subject,
            message,
            sender,
            [user_email],
            html_message=html_message,
            fail_silently=False,
        )
        log.info(f"Email sent to send the booking mail for the user: {user_email}")
        success_msg = f"<p>A Booking Mail will be sent to your e-mail <b> {user_email} </b> soon, check your Inbox!</p>Thank you"
        return True, success_msg
    except Exception as e:
        log.error(
            f"Error sending email to user {user_email} "
            + ERR_TEMPLATE.format(type(e).__name__, e.args)
        )
        return False, f"Failed to send booking email to user {user_email}: {e}"


def async_send_booking_mail(
    booking_obj,
    user_email,
    qcluster_name=settings.Q_CLUSTER_DEFAULT_QUEUE,
    group_name="Maktabiya_Booking_Mail",
    task_name=None,
):
    log.info(f"Sending booking email asynchronously for the user: {user_email}")
    mail_context = dict(
        user=booking_obj.user,
        office=booking_obj.office,
        room=booking_obj.room,
        desk=booking_obj.desk,
        date=booking_obj.booked_on,
        MYBOOK_URL=settings.MYBOOK_URL,
    )

    email_message = get_email_message(mail_context)
    subject = email_message.get("subject")
    message = email_message.get("message")
    html_message = email_message.get("html_message")
    sender = email_message.get("sender")

    log.debug("Sending booking email will set as an Async Task via Queue system!")

    task_id = async_task(
        "django.core.mail.send_mail",
        subject,
        message,
        sender,
        [user_email],
        html_message=html_message,
        fail_silently=False,
        cluster=qcluster_name,
        group=group_name,
        task_name=task_name or f"Booking Mail Task for {mail_context.get('user')}",
        hook="app_core.tasks.email_task_hook",
    )
    log.info(
        f"An Async Task has been initiated with id: [{task_id}] to send the booking mail for the user: {user_email}"
    )
    msg = f"<p>A Booking Mail will be sent to your e-mail <b> {user_email} </b> soon, check your Inbox!</p>Thank you"

    return True, msg


def get_email_message(mail_context):
    try:
        log.debug("Using HTML Template for rendering data")
        mail_template = EmailTemplate.objects.get(name=EMAIL_TEMPLATE_NAME)
        return dict(
            sender=mail_template.get_sender(),
            subject=mail_template.render_subject(mail_context),
            message=mail_template.render_plain_message(mail_context),
            html_message=mail_template.render_html_text(mail_context),
        )
    except ObjectDoesNotExist:
        log.warning(
            f"Email Template Doesn't Exist with name: {EMAIL_TEMPLATE_NAME}, default plain text will be used for email"
        )
        return dict(
            subject=f"Maktabiya, Work Desk Has Been Booked Successfully For The Date { mail_context.get('date') }",
            sender=settings.DEFAULT_FROM_EMAIL,
            message="""Hi {user},
    You have successfully booked for the office {office} in the room {room} for the desk {desk} on {date}
    You can check your bookings at: {MYBOOK_URL}
    Thanks and Best Regards,
    Maktabiya, A Desk Booking App!""".format(**mail_context),
            html_message="",
        )


def booking_desk(context):

    user = context.get("user")
    office = context.get("office")
    room = context.get("room")
    desk = context.get("desk")
    date = context.get("date")
    try:
        log.info(f"Booking the desk for user: {user}")
        # raise Exception("Simulated Exception for testing error handling in booking process")  # Simulate an exception for testing

        obj = Booking.objects.create(
            user=user,
            desk_id=desk.id,
            booked_on=date,
            room=room,
            office=office,
        )
        sucess_msg = f"<p>Dear <b>{user.username},</b></p><p>You have successfully booked a desk for the office <b> {office.name} </b> on <b>{date} </b> in the room <b>{room.name} </b></p>Thank you"

        log.info(
            f"Booked Successfully for user: {user} {office.name} - {room.name} - {desk.name} on {date}"
        )
        return True, obj, sucess_msg
    except Exception as e:
        log.error(
            "Failed to booking " + ERR_TEMPLATE.format(type(e).__name__, e.args),
            extra={"booking details": context},
        )
        err_msg = f"<p>Dear <b>{user.username},</b></p><p>Sorry but Booking Process <b>FAILED</b> for the office <b> {office.name} </b> on the date <b>{date} </b> in the room  <b>{room.name} </b></p>Excuse Us! It can happen :)"
        log.debug("Booking process FAILED, redirecting to the home page!")
        return False, None, err_msg


def check_booking_limit(request, date, booked):
    book_settings = Setting.objects.first()

    week_start = datetime.strptime(date, "%Y-%m-%d")
    week_start -= timedelta(days=week_start.weekday())
    week_end = week_start + timedelta(days=6)

    user_booked_per_week = request.user.booking_user.filter(
        booked_on__range=[week_start, week_end]
    ).count()

    log.debug(
        f"Check if the user has not reached the weekly limit, Total {user_booked_per_week} Booked from the User in the the Week {week_start}-{week_end} "
    )
    if user_booked_per_week >= book_settings.bookings_per_user_per_week:
        log.warning(
            f"User has reached week quota limit: {book_settings.bookings_per_user_per_week}"
        )
        return True, {"error": "user_booking_exceeded"}

    log.debug("Check if user has reached the day slot available")
    if booked.count() >= book_settings.bookings_per_day:
        log.warning("Reached the quota limit of the day booking...")
        return True, {"error": "booking_exceeded"}

    return False, {}  # No limit exceeded, return False with empty context
