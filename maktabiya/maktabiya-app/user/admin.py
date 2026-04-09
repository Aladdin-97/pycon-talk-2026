from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from user.models import Manager

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_display = [
        "username",
        "email",
        "last_login",
        "manager",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    list_per_page = 20
    readonly_fields = ("last_login", "date_joined")
    fieldsets = (
        ("Access Info", {"fields": ("username", "password")}),
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "manager",
                    "avatar",
                    "booking_visible",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            "New User Info",
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "is_active",
                    "is_staff",
                    "groups",
                ),
            },
        ),
    )


# Create the Manager inline form
class ManagerInline(admin.TabularInline):
    model = Manager
    extra = 1


# Register the Manager model with the admin site
@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "surname", "email")
    search_fields = list_display


admin.site.register(User, CustomUserAdmin)
