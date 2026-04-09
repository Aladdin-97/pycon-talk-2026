from django.urls import path

from .views import user_login, user_logout, profile

app_name = "user"
urlpatterns = [
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("profile/", profile, name="profile"),
]
