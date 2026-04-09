from django.conf import settings
from django.db.models.signals import post_migrate, post_save, pre_save
from django.dispatch import receiver
from django.core.management import call_command
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from django_q.tasks import Schedule
from maktabiya.settings import env
from app_core.models import Setting, Office, Room, Desk
from user.models import Manager
from email_templates.models import EmailTemplate
from names_generator import generate_name

import logging

log = logging.getLogger(f"{settings.APP_LOGGER}.{__name__}")
ERR_TEMPLATE = "An exception of type {0} occurred. Arguments:\n{1!r}"

DEFAULT_OFFICE_NAME = "[Default] Maktabiya Office"
DEFAULT_ROOM_NAME = "[Default] Maktabiya Room"
DEFAULT_DESK_COUNT = 4


@receiver(post_migrate)
def create_default_setting(sender, **kwargs):
    if sender.name == "app_core":
        log.info("Creating default office If Not Exist...")
        office, created = Office.objects.get_or_create(
            name=DEFAULT_OFFICE_NAME,
        )
        if created:
            log.info("Creating default room If Not Exist...")
            Room.objects.get_or_create(
                name=DEFAULT_ROOM_NAME, no_of_desk=DEFAULT_DESK_COUNT, office=office
            )

        if not Setting.objects.exists():
            log.info("Creating default settings If Not Exist...")
            Setting.objects.create(
                bookings_per_day=20,
                bookings_per_user_per_week=5,
            )


@receiver(post_migrate)
def create_default_email_templates(sender, **kwargs):
    if sender.name == "email_templates":
        log.info("Creating default post booking mail If Not Exist...")
        EmailTemplate.objects.get_or_create(
            name="Post Booking Mail",
            description="Send a mail after successful booking",
            subject="Maktabiya, Work Desk Has Been Booked Successfully For The Date {{ date }}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            active=True,
            plain_message="""Hi {{ user }},
You have successfully booked for the office {{ office }} in the room {{ room }} for the desk {{ desk }} on {{ date }}
You can check your bookings at: {{ MYBOOK_URL }}
Thanks and Best Regards,
Maktabiya, A Desk Booking App!""",
            html_template="email_templates/emails/book_mail.html",
        )

        log.info("Creating default Reminder mail If Not Exist...")
        EmailTemplate.objects.get_or_create(
            name="Reminder Mail",
            description="Booking Reminder Email Template",
            subject="Maktabiya, Reminder Booking Date {{ date }}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            active=True,
            plain_message="""Hi {{ user }},
Just a reminder for your booking in the {{ office }} in the room {{ room }} for the date {{ date }}.
Sukran and Have a Nice Day :)
Maktabiya, A Desk Booking App!""",
            html_template="email_templates/emails/reminder_mail.html",
        )

        log.info("Creating default Report Mail If Not Exist...")
        EmailTemplate.objects.get_or_create(
            name="Report Mail",
            description="Booking Report To Manager Email Template",
            subject="Maktabiya, Monthly Report Of Presence {{ year }}/{{ month }}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            active=True,
            plain_message="""Dear {{ manager }},
Here is your report of presence {{ year }}/{{ month }} \n\n
{{ csv_report }}
\nIn the attachment you can find the csv file: {{ csv_file }}
Sukran and Have a Nice Day :)
Maktabiya, A Desk Booking App.""",
            html_template="email_templates/emails/report_mail.html",
        )


@receiver(post_migrate)
def create_default_schedule_tasks(sender, **kwargs):
    # Get the current UTC time as a timezone-aware datetime object
    today = datetime.now(ZoneInfo("UTC"))
    # Replace the hour and minute to set the first run
    first_run_time = today.replace(hour=14, minute=0, second=0, microsecond=0)
    # If it is already past 2pm, set the first run for tomorrow at 2pm
    if today > first_run_time:
        first_run_time += timedelta(days=1)
    if sender.name == "django_q":
        log.info("Creating Reminder Mail Tasks If Not Exist...")

        log.debug(f"The Reminder Mail Tasks first will set as at {first_run_time}")
        if not Schedule.objects.filter(
            name="Maktabiya Task | Send Reminder Mail To User"
        ).exists():
            Schedule.objects.create(
                name="Maktabiya Task | Send Reminder Mail To User",
                func="app_core.tasks.send_reminder_mail_to_user",
                schedule_type=Schedule.DAILY,
                repeats=-1,  # -1 = forever
                cluster=settings.Q_CLUSTER_DEFAULT_QUEUE,
                next_run=first_run_time,
                hook="app_core.tasks.email_task_hook",
            )

        log.info("Creating Report Mail To Manager Tasks If Not Exist...")

        # Create a datetime object for the 3rd day of the month
        first_run_time = datetime(
            today.year,
            today.month,
            3,
            hour=12,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=ZoneInfo("UTC"),
        )
        # Check if first_run_time has already passed
        if first_run_time < today:
            # If passed, move to the 3rd day of the next month
            if today.month == 12:  # Handle December case
                next_month = 1
                next_year = today.year + 1
            else:
                next_month = today.month + 1
                next_year = today.year
            # Update first_run_time to the 3rd of next month
            first_run_time = datetime(
                next_year, next_month, 3, 12, 0, 0, tzinfo=ZoneInfo("UTC")
            )

        log.debug(
            f"The Report Mail To Manager Tasks first will set as at {first_run_time}"
        )
        if not Schedule.objects.filter(
            name="Maktabiya Task | Send Report To Manager"
        ).exists():
            Schedule.objects.create(
                name="Maktabiya Task | Send Report To Manager",
                func="app_core.tasks.send_report_mail_to_manager",
                schedule_type=Schedule.MONTHLY,
                repeats=-1,  # -1 = forever
                cluster=settings.Q_CLUSTER_LONG_QUEUE,
                next_run=first_run_time,
                hook="app_core.tasks.email_task_hook",
            )


@receiver(post_migrate)
def create_demo_data(sender, **kwargs):

    DEMO_OFFICES = ["Dhaka HQ", "Rome Office", "London Office"]

    if sender.name == "app_core" and env("CREATE_DEMO_DATA", default=False):
        log.info("Setting up demo office data...")
        counter = 1
        for office_name in DEMO_OFFICES:
            try:
                call_command(
                    "setup_workspace",
                    office_name,
                    rooms=counter,
                    desks=counter * DEFAULT_DESK_COUNT,
                )
                log.info(f"Demo data setup completed for office: {office_name}")
                counter += 1
            except Exception as e:
                log.error(
                    f"Error while setting up demo data for office {office_name} {ERR_TEMPLATE.format(type(e).__name__, e.args)}",
                    exc_info=True,
                )

    if sender.name == "booking" and env("CREATE_DEMO_DATA", default=False):
        log.info("Creating demo booking data...")

        demo_manager, _ = Manager.objects.get_or_create(
            email="manager@AladinStudioX.app",
            defaults={"name": "Aladin", "surname": "StudioX"},
        )
        demo_user_count = len(DEMO_OFFICES) * DEFAULT_DESK_COUNT
        try:
            call_command(
                "seed_bookings",
                user_count=demo_user_count,
                bookings_per_day=demo_user_count**DEFAULT_DESK_COUNT,
                manager_email=demo_manager.email,
            )
            log.info("Demo booking data setup completed.")
        except Exception as e:
            log.error(
                f"Error while setting up demo data for offices {DEMO_OFFICES}: {ERR_TEMPLATE.format(type(e).__name__, e.args)}",
                exc_info=True,
            )


@receiver(post_save, sender=Room)
def create_desk(sender, instance, created, **kwargs):
    if created:
        log.info(
            f"Room {instance.name} has been created, now {instance.no_of_desk} desks will be created"
        )
        Desk.objects.bulk_create(
            [
                Desk(room_id=instance.id, name=generate_name())
                for _ in range(instance.no_of_desk)
            ]
        )


@receiver(pre_save, sender=Room)
def pre_update_desks(sender, instance, **kwargs):
    """
    When update desk number in a room.
    Do a pre-check and
    Create new desk of no_of_desk > actual no of desk.
    Delete desk if no_of_desk < actual no of desk.
    Don't delete desk has been already book.
    """

    if instance.id is not None:
        # Existing room being updated
        room = sender.objects.get(pk=instance.id)
        desks_count = room.desks.count()

        if instance.no_of_desk > desks_count:
            num_desks_to_create = instance.no_of_desk - desks_count
            log.info(
                f"Desk Number changed for the room: {room.name}, will be created {num_desks_to_create} desks more"
            )

            Desk.objects.bulk_create(
                [
                    Desk(room=instance, name=generate_name())
                    for _ in range(1, num_desks_to_create + 1)
                ]
            )
        elif instance.no_of_desk < desks_count:
            num_desks_to_delete = desks_count - instance.no_of_desk
            desks_to_delete = instance.desks.filter(booking_desk__isnull=True)[
                :num_desks_to_delete
            ]
            log.warning("Only Desk which has no booking will be deleted...")
            log.info(
                f"Desk Number changed for the room: {room.name}, requested {num_desks_to_delete} but will be deleted {desks_to_delete} desks"
            )

            for desk in desks_to_delete:
                try:
                    desk.delete()
                except Exception as e:
                    log.error(
                        f"Error while deleting desk {ERR_TEMPLATE.format(type(e).__name__, e.args)}"
                    )

            # TODO: Better handling to not delete the desk which are booked, possibily show error at the admin side.
            # for now, override the num numbers to desk which can't and should not be deleted
            instance.no_of_desk = len(
                instance.desks.filter(booking_desk__isnull=False)
            ) + len(instance.desks.filter(booking_desk__isnull=True))
