# File: your_app/management/commands/seed_bookings.py
import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from datetime import date, timedelta
from booking.models import Desk, Booking
from user.models import Manager

User = get_user_model()


class Command(BaseCommand):
    help = "Populates the database with random bookings for users."

    def add_arguments(self, parser):
        parser.add_argument(
            "--user-count", type=int, default=10, help="Number of users to create/use"
        )
        parser.add_argument(
            "--office",
            type=str,
            default="all",
            help="Office name to book in (default: all)",
        )
        parser.add_argument(
            "--bookings-per-day", type=int, default=5, help="Target bookings per day"
        )
        parser.add_argument(
            "--manager-email",
            type=str,
            help="Email of the manager to assign bookings to",
        )

    def handle(self, *args, **options):
        user_count = options["user_count"]
        office_name = options["office"]
        per_day = options["bookings_per_day"]
        manager_email = options["manager_email"]

        # 1. Ensure Users exist
        self.stdout.write("Preparing users...")
        users = []
        for i in range(user_count):
            username = f"User{i+1}"
            defaults = {
                "email": f"{username}@AladinStudioX.app",
                "is_staff": False,
                "is_superuser": False,
                "manager": (
                    Manager.objects.get(email=manager_email) if manager_email else None
                ),
                "password": make_password(username),
                "first_name": username,
                "last_name": username,
            }
            user, _ = User.objects.get_or_create(username=username, defaults=defaults)
            users.append(user)

        # 2. Get Available Desks
        desks_qs = Desk.objects.all()
        if office_name != "all":
            desks_qs = desks_qs.filter(room__office__name=office_name)

        all_desks = list(desks_qs)
        if not all_desks:
            self.stdout.write(
                self.style.ERROR(f"No desks found for office: {office_name}")
            )
            return

        # 3. Populate Bookings
        # We'll cover Yesterday (-1), Today (0), Tomorrow (+1), skipping weekends
        today = date.today()
        potential_dates = [today - timedelta(days=1), today, today + timedelta(days=1)]

        # FILTRO WEEKEND: Escludiamo Sabato (5) e Domenica (6)
        dates_to_seed = [d for d in potential_dates if d.weekday() < 5]

        for target_date in dates_to_seed:
            self.stdout.write(
                f"Processing {target_date} ({target_date.strftime('%A')})..."
            )

            already_booked_desk_ids = Booking.objects.filter(
                booked_on=target_date
            ).values_list("desk_id", flat=True)

            already_booked_user_ids = Booking.objects.filter(
                booked_on=target_date
            ).values_list("user_id", flat=True)

            available_desks = [
                d for d in all_desks if d.id not in already_booked_desk_ids
            ]
            available_users = [u for u in users if u.id not in already_booked_user_ids]

            if not available_desks or not available_users:
                self.stdout.write(
                    self.style.WARNING(
                        f"   No free desks or users left for {target_date}"
                    )
                )
                continue

            # Determiniamo quanti booking creare per oggi
            num_to_book = min(len(available_desks), len(available_users), per_day)

            # Selezione casuale per varietà nella demo
            selected_desks = random.sample(available_desks, num_to_book)
            selected_users = random.sample(available_users, num_to_book)

            bookings_to_create = []

            for desk, random_user in zip(selected_desks, selected_users):
                bookings_to_create.append(
                    Booking(
                        desk=desk,
                        user=random_user,
                        office=desk.room.office,
                        room=desk.room,
                        booked_on=target_date,
                    )
                )

            Booking.objects.bulk_create(bookings_to_create)
            self.stdout.write(
                self.style.SUCCESS(
                    f"   Created {len(bookings_to_create)} unique bookings for {target_date}"
                )
            )

        # Log finale aggiornato
        skipped_count = len(potential_dates) - len(dates_to_seed)
        if skipped_count > 0:
            self.stdout.write(
                self.style.HTTP_INFO(f"Skipped {skipped_count} weekend days.")
            )

        self.stdout.write(
            self.style.SUCCESS("\nData population finished successfully.")
        )
