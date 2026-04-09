import threading
from django.test import TransactionTestCase
from django.db import connection, transaction, IntegrityError
from django.contrib.auth import get_user_model
from app_core.models import Desk, Office, Room
from booking.models import Booking
from datetime import date

User = get_user_model()


class TestBookingConcurrency(TransactionTestCase):
    def setUp(self):
        # Setup basic data
        self.user1 = User.objects.create(username="user1")
        self.user2 = User.objects.create(username="user2")
        self.office = Office.objects.create(
            name="Maktabiya Office",
        )
        self.room = Room.objects.create(
            name="Maktabiya Room", no_of_desk=1, office=self.office
        )
        self.desk = Desk.objects.get(id=1)
        self.booking_date = date(2026, 3, 1)

    def test_race_condition(self):
        results = []

        def make_booking(user):
            # Important: Each thread needs its own DB connection
            connection.close()
            try:
                # We don't check 'if exists'. We just TRY to create.
                # The UniqueConstraint in your Model will block the second one.
                Booking.objects.create(
                    user=user,
                    desk=self.desk,
                    booked_on=self.booking_date,
                    room=self.room,
                    office=self.office,
                )

                results.append("SUCCESS")
            except IntegrityError:
                # This is triggered by your UniqueConstraint
                results.append("BLOCKED")
            except Exception as e:
                results.append(f"ERROR: {type(e).__name__}")

        # Create two threads attempting to book at the exact same time
        thread1 = threading.Thread(target=make_booking, args=(self.user1,))
        thread2 = threading.Thread(target=make_booking, args=(self.user2,))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        # Debug print to see what happened in the console
        print(f"\nThread Results: {results}")

        # ASSERTIONS
        # Exactly one should succeed
        self.assertEqual(
            results.count("SUCCESS"), 1, "Only one booking should succeed."
        )
        # Exactly one should be blocked by the UniqueConstraint
        self.assertEqual(
            results.count("BLOCKED"),
            1,
            "One booking should have been blocked by IntegrityError.",
        )
        # Ensure only 1 row exists in the DB
        self.assertEqual(
            Booking.objects.filter(desk=self.desk, booked_on=self.booking_date).count(),
            1,
        )
