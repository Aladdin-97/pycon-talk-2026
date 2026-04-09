from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections, OperationalError

import time


class Command(BaseCommand):
    help = "Wait for the database and ensure the specified table is ready for read operations"

    def handle(self, *args, **options):
        self.stdout.write("Checking readiness for Maktabiya Database ...")
        db_conn = connections["default"]
        connected = False
        while not connected:
            try:
                with db_conn.cursor() as cursor:
                    # Perform a simple SELECT query on a specific table
                    cursor.execute("SELECT 1;")
                connected = True
                self.stdout.write(
                    self.style.SUCCESS(
                        "Database and table are ready for read/write operations!"
                    )
                )
            except OperationalError as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Maktabiya Database not ready ({e}), waiting {settings.DB_CHECK_SLEEP_DURATION} seconds..."
                    )
                )
                time.sleep(settings.DB_CHECK_SLEEP_DURATION)
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(
                        f"Maktabiya Database Unexpected error: {e}, waiting {settings.DB_CHECK_SLEEP_DURATION} seconds..."
                    )
                )
                time.sleep(settings.DB_CHECK_SLEEP_DURATION)
