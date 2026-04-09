import time
from django.core.management.base import BaseCommand
from django.conf import settings
from booking.tasks import async_send_booking_mail
from booking.models import Booking


class Command(BaseCommand):
    help = (
        "Benchmark that separates Dispatch from Execution even when workers are live."
    )

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, nargs="?", default=100)
        parser.add_argument(
            "--qcluster", type=str, default=settings.Q_CLUSTER_DEFAULT_QUEUE
        )

    def handle(self, *args, **options):
        task_count = options["count"]
        cluster_tasks = {options["qcluster"]: options["count"]}
        mail_context = Booking.objects.first()

        self.stdout.write(self.style.SUCCESS(f"🚀 Adding {task_count} tasks..."))

        for cluster_key, task_count in cluster_tasks.items():
            dispatch_start = time.time()
            for loop_count in range(task_count):
                async_send_booking_mail(
                    booking_obj=mail_context,
                    user_email="aladin@AladinStudioX.app",
                    qcluster_name=cluster_key,
                    group_name=f"{cluster_key}_{task_count}",
                    task_name=f"Benchmark Task - {loop_count} of {task_count}",
                )
        dispatch_end = time.time()
        dispatch_total = dispatch_end - dispatch_start
        self.stdout.write(
            f"Dispatch Finished ({dispatch_total:.2f}s). Check Workers...\n"
        )
