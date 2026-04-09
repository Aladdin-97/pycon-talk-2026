from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from datetime import date, timedelta

import logging

log = logging.getLogger(f"{settings.APP_LOGGER}.{__name__}")
ERR_TEMPLATE = "An exception of type {0} occurred. Arguments:\n{1!r}"


try:
    from django_q.models import OrmQ, Task

    DJANGO_Q_AVAILABLE = True
except ImportError:
    DJANGO_Q_AVAILABLE = False

try:
    from booking.models import Booking, Desk, Office, Room

    BOOKING_AVAILABLE = True
except ImportError:
    BOOKING_AVAILABLE = False


def _get_cluster_names() -> list:
    log.debug("Fetching cluster names from OrmQ and Task models")
    if not DJANGO_Q_AVAILABLE:
        log.warning("Django-Q is not available, returning empty cluster list")
        return []
    clusters = set()
    try:
        for v in OrmQ.objects.values_list("key", flat=True).distinct():
            if v:
                clusters.add(v)
        for v in Task.objects.values_list("cluster", flat=True).distinct():
            if v:
                clusters.add(v)
        log.debug(f"Successfully retrieved {len(clusters)} unique clusters: {clusters}")
        return sorted(clusters)
    except Exception as e:
        log.error(ERR_TEMPLATE.format(type(e).__name__, e.args), exc_info=True)
        return []


# ─────────────────────────────────────────────────────────────────────────────
# Booking data endpoint
# ─────────────────────────────────────────────────────────────────────────────


@staff_member_required
def dashboard_booking_data(request):
    """
    GET /admin/dashboard/booking-data/

    Params
    ------
    office_id   int | "all"   - filter bookings by office
    date_range  "today" | "yesterday" | "tomorrow" (default: "today")
    """
    log.debug(f"dashboard_booking_data called by user: {request.user}")

    if not BOOKING_AVAILABLE:
        log.error("Booking app is not available")
        return JsonResponse({"error": "booking app not available"}, status=503)

    # ── date logic ──────────────────────────────────────────────────────────
    today = date.today()
    date_range = request.GET.get("date_range", "today").lower().strip()
    log.debug(f"Date range query: {date_range}")

    if date_range == "yesterday":
        target_date = today - timedelta(days=1)
    elif date_range == "tomorrow":
        target_date = today + timedelta(days=1)
    else:
        target_date = today

    log.debug(f"Processing bookings for date: {target_date}")

    office_id = request.GET.get("office_id", "all").strip()
    log.debug(f"Office filter: {office_id}")

    # ── office filter ─────────────────────────────────────────────────────────
    office_filter = {}
    scoped_office_id = None
    if office_id != "all":
        try:
            scoped_office_id = int(office_id)
            office_filter = {"office_id": scoped_office_id}
            log.debug(f"Filtering to office_id: {scoped_office_id}")
        except (ValueError, TypeError) as e:
            log.warning(f"Invalid office_id provided: {office_id}. Error: {e}")
            pass

    # ── counts (Total infrastructure) ─────────────────────────────────────────
    try:
        if scoped_office_id:
            offices_qs = Office.objects.filter(id=scoped_office_id)
            rooms_qs = Room.objects.filter(office_id=scoped_office_id)
            desks_qs = Desk.objects.filter(room__office_id=scoped_office_id)
        else:
            offices_qs = Office.objects.all()
            rooms_qs = Room.objects.all()
            desks_qs = Desk.objects.all()

        total_offices = offices_qs.count()
        total_rooms = rooms_qs.count()
        total_desks = desks_qs.count()

        log.debug(
            f"Infrastructure counts - Offices: {total_offices}, Rooms: {total_rooms}, Desks: {total_desks}"
        )

        # ── filtered bookings ─────────────────────────────────────────────────────

        bookings_qs = Booking.objects.filter(booked_on=target_date, **office_filter)
        desks_booked = bookings_qs.values("desk_id").distinct().count()
        desks_free = max(total_desks - desks_booked, 0)

        log.debug(
            f"Booking stats for {target_date}: booked={desks_booked}, free={desks_free}, total={total_desks}"
        )

        if desks_booked == total_desks:
            log.warning(f"All desks are booked on {target_date}")
        elif desks_free == total_desks:
            log.debug(f"No desks are booked on {target_date}")

        offices_list = list(Office.objects.values("id", "name").order_by("name"))
        log.debug(f"Retrieved {len(offices_list)} offices for dropdown")

        return JsonResponse(
            {
                "target_date": target_date.isoformat(),  # useful for debug in UI
                "offices": total_offices,
                "rooms": total_rooms,
                "desks_total": total_desks,
                "desks_booked": desks_booked,
                "desks_free": desks_free,
                "offices_list": offices_list,
            }
        )
    except Exception as e:
        log.error(ERR_TEMPLATE.format(type(e).__name__, e.args), exc_info=True)
        return JsonResponse({"error": "Failed to fetch booking data"}, status=500)


# ─────────────────────────────────────────────────────────────────────────────
# Task data endpoint
# ─────────────────────────────────────────────────────────────────────────────


@staff_member_required
def dashboard_task_data(request):
    """
    GET /admin/dashboard/task-data/

    Params
    ------
    clusters[]  repeated - filter by cluster name (empty = all)
    """
    log.debug(f"dashboard_task_data called by user: {request.user}")

    if not DJANGO_Q_AVAILABLE:
        log.error("Django-Q is not available")
        return JsonResponse({"error": "django-q not available"}, status=503)

    selected_clusters = request.GET.getlist("clusters[]")
    log.debug(f"Selected clusters filter: {selected_clusters}")

    try:
        # ── queued tasks (OrmQ) ───────────────────────────────────────────────────
        log.debug("Fetching queued tasks from OrmQ")
        queued_total = 0
        queued_by_cluster: dict = {}

        orm_qs = OrmQ.objects.all()
        if selected_clusters:
            orm_qs = orm_qs.filter(key__in=selected_clusters)
            log.debug(f"Filtering OrmQ by clusters: {selected_clusters}")

        for q in orm_qs:
            cluster_name = q.key or "default"
            queued_total += 1
            queued_by_cluster[cluster_name] = queued_by_cluster.get(cluster_name, 0) + 1

        log.debug(
            f"Queued tasks total: {queued_total}, breakdown by cluster: {queued_by_cluster}"
        )

        # ── finished tasks (Task) ─────────────────────────────────────────────────
        log.debug("Fetching finished tasks from Task model")
        task_qs = Task.objects.all()
        if selected_clusters:
            task_qs = task_qs.filter(cluster__in=selected_clusters)
            log.debug(f"Filtering Task by clusters: {selected_clusters}")

        # Success Breakdown
        success_tasks = task_qs.filter(success=True)
        success_count = success_tasks.count()
        success_by_cluster = {}
        for t in success_tasks.values("cluster").order_by():
            c_name = t["cluster"] or "default"
            success_by_cluster[c_name] = success_by_cluster.get(c_name, 0) + 1

        log.debug(
            f"Successful tasks: {success_count}, breakdown by cluster: {success_by_cluster}"
        )

        # Failed Breakdown
        failed_tasks = task_qs.filter(success=False)
        failed_count = failed_tasks.count()
        failed_by_cluster = {}
        for t in failed_tasks.values("cluster").order_by():
            c_name = t["cluster"] or "default"
            failed_by_cluster[c_name] = failed_by_cluster.get(c_name, 0) + 1

        log.debug(
            f"Failed tasks: {failed_count}, breakdown by cluster: {failed_by_cluster}"
        )

        if failed_count > 0:
            log.warning(f"There are {failed_count} failed tasks")

        # ── queued colour ─────────────────────────────────────────────────────────
        queued_color = (
            "neutral"
            if queued_total == 0
            else ("yellow" if queued_total <= 10 else "red")
        )
        log.debug(f"Queued status color: {queued_color} (queued_total={queued_total})")

        cluster_names = _get_cluster_names()
        log.debug(f"Available clusters for dropdown: {cluster_names}")

        return JsonResponse(
            {
                "queued": queued_total,
                "queued_color": queued_color,
                "queued_by_cluster": queued_by_cluster,
                "success": success_count,
                "success_by_cluster": success_by_cluster,
                "failed": failed_count,
                "failed_by_cluster": failed_by_cluster,
                "available_clusters": cluster_names,
            }
        )
    except Exception as e:
        log.error(ERR_TEMPLATE.format(type(e).__name__, e.args), exc_info=True)
        return JsonResponse({"error": "Failed to fetch task data"}, status=500)
