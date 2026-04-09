import csv
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from io import StringIO
from datetime import datetime, timedelta
from django_q.tasks import fetch

from user.models import User
from booking.models import Booking
from email_templates.models import EmailTemplate


import logging

log = logging.getLogger(f"{settings.APP_LOGGER}.{__name__}")
ERR_TEMPLATE = "An exception of type {0} occurred. Arguments:\n{1!r}"

EMAIL_TEMPLATE_NAME_1 = "Reminder Mail"
EMAIL_TEMPLATE_NAME_2 = "Report Mail"


def valid_date(date, date_fmt="%Y-%m-%d"):
    log.info("Checking date validity for crontasks...")
    try:
        datetime.strptime(str(date), date_fmt)
    except ValueError:
        log.warning(f"Not a valid date: '{date}' for the {date_fmt}")
        return False

    return True


def send_reminder_mail_to_user(start_date=None, end_date=None):
    """Send reminder mail to user for the booking in the date range of start_date and end_date,
    if not provided it will send for the next day booking by default
    format for both is %Y-%m-%d, example: 2024-06-30
    """
    SUBJECT = "Maktabiya, Reminder booking date {date}"
    MESSAGE = """Hey, {user} ;),
Just a reminder for your booking in the office {office} in the room {room} for the desk {desk} on the date {date}.
Sukran and Have a Nice Day :)
Maktabiya, A desk booking app"""
    SENDER = "maktabiya-reminder@aladinstudiox.bd"
    mail_template = False

    log.info("Sending reminder mail to user")
    current_date = datetime.now().date()
    next_day = current_date + timedelta(days=1)
    check_dates = [valid_date(start_date, "%Y-%m-%d"), valid_date(end_date, "%Y-%m-%d")]

    if not any(check_dates):
        log.warning(
            f"Date passed in parameters are not valid, default {next_day} will be used..."
        )
        start_date = next_day
        end_date = next_day

    try:
        mail_template = EmailTemplate.objects.get(name=EMAIL_TEMPLATE_NAME_1)
        sender = mail_template.get_sender()
    except ObjectDoesNotExist:
        log.warning(
            f"Email Template Doesn't Exist with name: {EMAIL_TEMPLATE_NAME_1}, default plain text will be used for email"
        )

    log.info("Searching booking to send reminder mails...")
    bookings = Booking.objects.filter(
        booked_on__gte=start_date, booked_on__lte=end_date
    )
    log.debug(
        f"Bookings found for the day: {start_date} - {end_date}",
        extra={"Booking List": bookings},
    )
    if not bookings:
        log.warning(
            f"Empty Booking List for the date {start_date}-{end_date}, No Email Will Be Send"
        )
        return f"Empty Booking List for the date {start_date}-{end_date}, User Email Reminder has been Skipped today :)"

    send_status = []
    for book in bookings:
        book_id = book.id
        booked_date = book.booked_on
        user = book.user.username
        user_email = book.user.email
        room = book.room.name
        office = book.office.name
        desk = book.desk.name
        message = MESSAGE.format(
            user=user, office=office, room=room, desk=desk, date=booked_date
        )
        subject = (
            mail_template.render_subject(dict(date=booked_date))
            if mail_template
            else SUBJECT.format(date=booked_date)
        )
        html_message = (
            mail_template.render_html_text(
                dict(
                    book_id=book_id,
                    user=user,
                    office=office,
                    room=room,
                    desk=desk,
                    date=booked_date,
                    MYBOOK_URL=settings.MYBOOK_URL,
                )
            )
            if mail_template
            else ""
        )
        status = send_mail(
            subject,
            message,
            sender if mail_template else SENDER,
            [user_email],
            html_message=html_message,
            fail_silently=False,
        )
        send_status.extend([{user_email: status}])

    return tuple(send_status)


def send_report_mail_to_manager(month=None, year=None):
    # Assuming cron task running in the next month, get the previous month
    log.info("Sending report mail to manager")
    today = datetime.today()
    last_month = (today - timedelta(days=today.day)).replace(day=1)
    check_dates = [valid_date(month, "%m"), valid_date(year, "%Y")]
    if not any(check_dates):
        log.warning(
            f"Date passed in parameters are not valid, default {last_month} will be used..."
        )
        month = last_month.month
        year = last_month.year

    # Define the year and month for filtering
    SENDER = "maktabiya-report@aladinstudiox.bd"
    SUBJECT = f"Maktabiya, Monthly Report Of Presence {year}/{month}"
    MESSAGE = """Dear {manager},
Here is your report of presence {year}/{month} \n\n
{csv_report}
\nIn the attachment you can find the csv file: {csv_file}
Sukran and Have a Nice Day :)
Maktabiya, A Desk Booking App."""

    mail_template = False
    try:
        mail_template = EmailTemplate.objects.get(name=EMAIL_TEMPLATE_NAME_2)
        sender = mail_template.get_sender()
    except ObjectDoesNotExist:
        log.warning(
            f"Email Template Doesn't Exist with name: {EMAIL_TEMPLATE_NAME_2}, default plain text will be used for email"
        )

    log.info("Searching booking to send report mails...")

    # Filter the bookings by year and month
    filtered_bookings = Booking.objects.filter(
        booked_on__year=year, booked_on__month=month
    )
    log.debug(
        f"Filtering bookings for the date {year}/{month}",
        extra={"filtered_bookings": filtered_bookings},
    )
    # Annotate the User objects with the count of their bookings for the specified year and month
    users_with_booking_count = User.objects.filter(
        booking_user__in=filtered_bookings
    ).annotate(num_bookings=Count("booking_user"))
    log.debug(
        f"Users with bookings for the date {year}/{month}",
        extra={"users_with_booking_count": users_with_booking_count},
    )
    # Group users by manager and their booking counts
    manager_user_booking_dict = {}
    for user in users_with_booking_count:
        manager = user.manager
        if manager:
            if manager not in manager_user_booking_dict:
                manager_user_booking_dict[manager] = []
            manager_user_booking_dict[manager].extend([(user, user.num_bookings)])
        else:
            log.warning(
                f"Skipping user {user.username} as they do not have a manager related on DB."
            )

    log.debug(
        "Manager with their employess presence data",
        extra={"data_dict": manager_user_booking_dict.items()},
    )
    if not manager_user_booking_dict:
        log.warning("Empty value for manager and employes, No Email Will Be Send")
        return f"Empty values for the {year}/{month}, Email Report has been skipped for this month "

    send_status = []
    # Send emails to each manager
    # NOTE: Only user which have a manager related will be reported
    for manager, user_booking_list in manager_user_booking_dict.items():
        # Create a CSV string for the related users and booking count
        csv_data = StringIO()
        csv_writer = csv.writer(csv_data, delimiter=";")
        csv_writer.writerow(["Name", "Surname", "Email", "Booked Count"])
        for user, booking_count in user_booking_list:
            csv_writer.writerow(
                [user.first_name, user.last_name, user.email, booking_count]
            )
        # Create the email content
        csv_report = csv_data.getvalue()
        csv_file = f"Maktabiya_booking_report_{year}_{month}.csv"
        mail_context = dict(
            manager=f"{manager.name} {manager.surname}",
            year=year,
            month=month,
            csv_report=csv_report,
            csv_file=csv_file,
        )
        sender = sender if mail_template else SENDER
        subject = (
            mail_template.render_subject(dict(year=year, month=month))
            if mail_template
            else SUBJECT
        )
        html_message = (
            mail_template.render_html_text(mail_context) if mail_template else ""
        )

        message = MESSAGE.format(**mail_context)
        # Send the email to the manager with CSV attachment
        email = EmailMultiAlternatives(
            subject, message, from_email=sender, to=[manager.email]
        )
        email.attach_alternative(html_message, "text/html")
        log.info("Attaching the report to the mail")
        email.attach(csv_file, csv_data.getvalue(), "text/csv")
        log.info("Sending report to the manager")
        status = email.send()
        send_status.extend([{manager.email: status}])

    return tuple(send_status)


def email_task_hook(task):
    """This hook avoid to save the HTML MESSAGE on DB when task is successful"""

    log.info(f"Starting email_task_hook with task: {task.name} - {task.id}")
    fetch_task = fetch(task.id)
    if fetch_task and fetch_task.success:
        try:
            log.debug("Updating email_task_hook to not save html message on DB")

            # set the hook function to None, otherwise it loops
            # levelname": "ERROR", "message": "return hook app_core.tasks.email_task_hook failed on [admin] because maximum recursion depth exceeded in comparison
            fetch_task.hook = None
            fetch_task.kwargs["html_message"] = None
            fetch_task.save()

        except Exception as e:
            log.warning(
                f"Error while updating email_task_hook: {task.name} - {task.id}: {e}"
            )
