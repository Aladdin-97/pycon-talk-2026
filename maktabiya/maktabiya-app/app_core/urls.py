from django.urls import path
from app_core.views import dashboard_booking_data, dashboard_task_data

app_name = "app_core"
urlpatterns = [
    path("booking-data/", dashboard_booking_data, name="admin-dashboard-booking"),
    path("task-data/", dashboard_task_data, name="admin-dashboard-tasks"),
]
