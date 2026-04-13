import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.core.management.base import BaseCommand
from django.conf import settings
from booking.tasks import async_send_booking_mail
from booking.models import Booking


def _dispatch_task(args):
    booking_obj, user_email, cluster_key, task_count, loop_count = args
    async_send_booking_mail(
        booking_obj=booking_obj,
        user_email=user_email,
        qcluster_name=cluster_key,
        group_name=f"{cluster_key}_{task_count}",
        task_name=f"Benchmark Task - {loop_count} of {task_count}",
    )
    return loop_count


class Command(BaseCommand):
    help = "Benchmark that dispatches tasks in parallel using ThreadPoolExecutor."

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, nargs="?", default=100)
        parser.add_argument(
            "--qcluster", type=str, default=settings.Q_CLUSTER_DEFAULT_QUEUE
        )
        parser.add_argument(
            "--threads",
            type=int,
            default=4,
            help="Number of threads to use for dispatching (default: 4)",
        )

    def handle(self, *args, **options):
        task_count = options["count"]
        cluster_key = options["qcluster"]
        threads = options["threads"]
        mail_context = Booking.objects.first()

        self.stdout.write(
            self.style.SUCCESS(
                f"🚀 Dispatching {task_count} tasks across {threads} threads..."
            )
        )

        task_args = [
            (mail_context, "aladin@AladinStudioX.app", cluster_key, task_count, i)
            for i in range(task_count)
        ]

        dispatch_start = time.time()
        completed = 0
        failed = 0

        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {executor.submit(_dispatch_task, arg): arg for arg in task_args}
            for future in as_completed(futures):
                try:
                    loop_count = future.result()
                    completed += 1
                    self.stdout.write(
                        f"  ✅ Dispatched task {loop_count} of {task_count}"
                    )
                except Exception as e:
                    failed += 1
                    self.stdout.write(self.style.ERROR(f"  ❌ Failed: {e}"))

        dispatch_end = time.time()
        dispatch_total = dispatch_end - dispatch_start

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDispatch Finished ({dispatch_total:.2f}s)\n"
                f"  ✅ Completed: {completed}\n"
                f"  ❌ Failed:    {failed}\n"
                f"  ⚡ Rate:      {completed / dispatch_total:.1f} tasks/sec\n"
                f"\nCheck Workers..."
            )
        )
