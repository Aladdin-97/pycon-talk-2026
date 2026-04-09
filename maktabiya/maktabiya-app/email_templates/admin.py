from django.contrib import admin

from email_templates.models import EmailTemplate


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "subject",
        "active",
    )
    search_fields = ("name",)
