from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, F
from django.db import transaction
from django.shortcuts import render, redirect
from django_htmx.http import HttpResponseClientRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.safestring import mark_safe
from app_core.models import Desk, Room, Office
from booking.models import Booking
from booking.tasks import (
    async_send_booking_mail,
    sync_send_booking_mail,
    booking_desk,
    check_booking_limit,
)


import logging

log = logging.getLogger(f"{settings.APP_LOGGER}.{__name__}")
ERR_TEMPLATE = "An exception of type {0} occurred. Arguments:\n{1!r}"
EMAIL_TEMPLATE_NAME = "Post Booking Mail"


@login_required(login_url="/user/login/")
def index(request):
    offices = Office.objects.all()
    log.debug(f"Extracted office data for the form: {offices}")
    if request.method != "POST":
        return render(request, "booking/index.html", {"offices": offices})

    date = request.POST.get("date")
    office_id = request.POST.get("office")
    log.debug(f"Requesting Desk for the Date: {date} and Office ID: {office_id}")
    request.session["date"] = date
    request.session["office"] = office_id

    booked = Desk.objects.filter(booking_desk__booked_on=date)
    limit_reached, error = check_booking_limit(request, date, booked)
    if limit_reached:
        return render(request, "service_unavailable.html", error)

    office = Office.objects.get(id=office_id)
    log.debug(f"Got from DB {office} - {booked}")

    log.info(f"Getting all available room for the office id: {office_id}")
    rooms = Room.objects.filter(office_id=office_id)
    rooms_desks = rooms.prefetch_related("desks").all().order_by("-id")
    rooms = rooms_desks.annotate(
        desks_empty=F("no_of_desk")
        - Count("desks", filter=Q(desks__booking_desk__booked_on=date))
    )
    log.debug(f"Rooms available: {rooms}")

    context = {
        "booked": booked,
        "rooms": rooms,
        "date": date,
        "offices": offices,
        "office": office,
        "submitted": True,
    }
    log.debug("Context data for rendering html", extra=context)
    return render(request, "booking/index.html", context)


@login_required(login_url="/user/login/")
def book(request, desk_id, room_id, office_id):
    # print(desk_id, room_id, office_id)
    desk = Desk.objects.get(id=desk_id)
    user = request.user
    office = Office.objects.get(id=office_id)
    room = Room.objects.get(id=room_id)
    date = request.session.get("date")
    log.info(f"Booking in {office.name} - {room.name} - {desk.name} on {date}")

    context = {
        "date": date,
        "desk": desk,
        "room": room,
        "office": office,
        "user": user,
    }

    log.debug(
        "Double Check in the backend if user is trying to book the desk for the same day, ayo!"
    )
    if Booking.objects.filter(booked_on=date, user=user).exists():
        log.warning(
            f"Double Checked Efficient! {user.username} Already booked the date {date}...ayo!"
        )

        messages.warning(
            request,
            f"<p>Dear <b>{user.username}</b>, You have already booked a desk for the date <b>{date}</b>.<br>Go to <a type='button' class='btn btn-outline-warning btn-sm text-dark' href='/my-bookings'>My Bookings</a> to see all your bookings. <br>Thanks ;)",
            extra_tags="alert alert-warning",
        )
        return HttpResponseClientRedirect("/")

    # print(context)
    if request.method != "POST":
        log.info("Confirm booking in the modal window", extra=context)
        return render(request, "booking/fragments/confirm_book_modal.html", context)

    status, booking_obj, msg = booking_desk(context)
    messages.info(
        request,
        mark_safe(msg),  # Mark the message as safe to allow HTML rendering
        extra_tags="alert alert-success" if status else "alert alert-danger",
    )
    if not status:
        log.debug("Booking process FAILED, redirecting to the home page!")
        return HttpResponseClientRedirect("/")

    log.info("Sending booking mail with details to the user")
    ### SYNC TASK ####
    # is_sent, msg = sync_send_booking_mail(booking_obj, user.email)
    ##################
    ### ASYNC TASK ###
    is_sent, msg = async_send_booking_mail(booking_obj, user.email)
    ##################
    messages.info(
        request,
        mark_safe(msg),  # Mark the message as safe to allow HTML rendering
        extra_tags="alert alert-info" if is_sent else "alert alert-danger",
    )

    log.debug("Booking process completed, redirecting to the home page!")
    return HttpResponseClientRedirect("/")


@login_required(login_url="/user/login/")
def my_bookings(request):
    # log.info(f"My bookings: {request}", extra={"user": request.user})
    # log.info(f"session {request.session.session_key}")
    me = request.user

    # Handle filtering by office and date if provided in POST data
    office_id = request.POST.get("office")
    date = request.POST.get("date")
    log.debug(
        f"Getting user booking list of the user: {me} date: {date} office_id: {office_id}"
    )

    # Filter bookings based on user and provided parameters ordered in descending order
    bookings = me.booking_user.select_related("desk__room").order_by("-booked_on")
    if office_id:
        bookings = bookings.filter(office_id=office_id)
    if date:
        bookings = bookings.filter(booked_on=date)

    # Use Paginator to paginate the query results
    paginator = Paginator(bookings, 5)  # Show 5 bookings per page

    page = request.GET.get("page")
    try:
        my_books = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        my_books = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        my_books = paginator.page(paginator.num_pages)

    return render(
        request,
        "booking/my_bookings.html",
        {
            "my_books": my_books,
            "offices": Office.objects.all(),
            "office": office_id,
            "date": date,
            "submitted": True if (office_id or date) else False,
        },
    )


@login_required(login_url="/user/login/")
def book_delete(request):
    if request.method != "POST":
        return redirect("booking:my-bookings")

    book_ids = request.POST.getlist("booking_ids[]")

    if not book_ids:
        log.info(
            f"No book Id in the request for user {request.user}, redirecting to my bookings!"
        )
        return redirect("booking:my-bookings")

    try:
        with transaction.atomic():
            to_delete = Booking.objects.filter(id__in=book_ids, user=request.user)

            deleted_count, _ = to_delete.delete()

            if deleted_count > 0:
                messages.success(
                    request,
                    f"Successfully deleted {deleted_count} booking(s).",
                    extra_tags="alert alert-success",
                )
            else:
                messages.warning(request, "No bookings were found to delete.")

    except Exception as e:
        log.exception("Bulk delete failed")
        messages.error(request, f"An error occurred while deleting the bookings: {e}")

    return redirect("booking:my-bookings")
