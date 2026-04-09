from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Check if a user exists"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="Username of the user to check")

    def handle(self, *args, **options):
        username = options["username"]
        User = get_user_model()
        user_exists = User.objects.filter(username=username).exists()

        if user_exists:
            self.stdout.write(self.style.SUCCESS(f"User [{username}] exists."))
            exit(0)
        else:
            self.stdout.write(self.style.WARNING(f"User [{username}] does not exist."))
            exit(1)
