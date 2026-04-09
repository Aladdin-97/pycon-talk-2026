import csv
import datetime
from django.contrib import admin
from django.http import HttpResponse
from rangefilter.filters import DateRangeFilter
from booking.models import Booking


# custom fix: https://github.com/EricOuma/django-jazzmin-admin-rangefilter/issues/13#issue-3473230511
class CustomDateRangeFilter(DateRangeFilter):
    def queryset(self, request, queryset):
        for key, value in self.form.data.items():
            if (
                key in [self.lookup_kwarg_gte, self.lookup_kwarg_lte]
                and type(value) == list
            ):
                self.form.data[key] = value[0]
        return super().queryset(request, queryset)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["user", "office", "room", "desk", "booked_on"]
    list_per_page = 20  # No of records per page

    actions = ["export_csv"]
    list_filter = [
        ("booked_on", CustomDateRangeFilter),
        ("user__username"),
        ("office__name"),
        ("room__name"),
    ]

    # If you would like to add a default range filter
    # method pattern "get_rangefilter_{field_name}_default"
    def get_rangefilter_booked_on_default(self, request):
        return (
            datetime.date.today,
            datetime.date.today() + datetime.timedelta(days=14),
        )

    def has_add_permission(self, request):
        return False

    def room_name(self, obj):
        return obj.room.name

    def office_name(self, obj):
        return obj.office.name

    @admin.action(description="Export as CSV")
    def export_csv(self, request, queryset):
        # Generate a timestamp to append to the filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        # Construct the filename with the timestamp
        filename = f"Maktabiya_Desk_Booking_Report_{timestamp}.csv"

        res = HttpResponse(content_type="text/csv")
        res["Content-Disposition"] = f"attachment; filename={filename}"

        writer = csv.writer(res)
        writer.writerow(
            [
                "Username",
                "Office name",
                "Room Name",
                "Desk Name",
                "Booked On",
            ]
        )
        for book in queryset:
            writer.writerow(
                [
                    book.user.username,
                    book.office.name,
                    book.desk.room.name,
                    book.desk.name,
                    book.booked_on,
                ]
            )

        return res
