from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _
from booking.models import Office, Room


class Command(BaseCommand):
    help = "Provisions a new office infrastructure with rooms and desks."

    def add_arguments(self, parser):
        # Positional argument
        parser.add_argument(
            "office_name", type=str, help="The name of the office to create"
        )

        # Optional arguments
        parser.add_argument(
            "--rooms", type=int, default=1, help="Number of rooms to generate"
        )
        parser.add_argument(
            "--desks", type=int, default=4, help="Number of desks per room"
        )

    def handle(self, *args, **options):
        office_name = options["office_name"]
        room_count = options["rooms"]
        desks_per_room = options["desks"]

        self.stdout.write(f"Starting workspace setup for: {office_name}...")

        # 1. Get or Create the Office
        office, created = Office.objects.get_or_create(name=office_name)
        status = "created" if created else "already exists"
        self.stdout.write(self.style.SUCCESS(f"Office '{office_name}' {status}."))

        for i in range(1, room_count + 1):
            # 2. Create the Room
            # Formatting as: "Rome Office Room 1"
            room_name = f"{office_name} Room {i}"
            room, r_created = Room.objects.get_or_create(
                name=room_name, office=office, defaults={"no_of_desk": desks_per_room}
            )

            if r_created:
                self.stdout.write(f"  - Created Room: {room_name}")
            else:
                room.no_of_desk = desks_per_room
                room.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"    * Successfully provisioned {desks_per_room} desks in {room_name}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(f"\nWorkspace setup completed for {office_name}.")
        )
