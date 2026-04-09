from django.contrib import admin
from app_core.models import Office, Room, Desk, Setting


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_per_page = 20  # No of records per page
    list_editable = ["name"]
    list_filter = ["name"]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["name", "no_of_desk", "office"]
    list_editable = ["no_of_desk"]
    list_filter = ["name", "no_of_desk", "office__name"]
    list_per_page = 20  # No of records per page


@admin.register(Desk)
class DeskAdmin(admin.ModelAdmin):
    list_editable = ["name"]
    list_display = ["id", "name", "room", "office_name"]
    list_filter = ["name", "room__name", "room__office__name"]
    list_per_page = 20  # No of records per page

    def has_add_permission(self, request):
        return False


@admin.register(Setting)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ["name", "bookings_per_day", "bookings_per_user_per_week"]
    list_editable = ["bookings_per_day", "bookings_per_user_per_week"]
    list_per_page = 20  # No of records per page

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False
