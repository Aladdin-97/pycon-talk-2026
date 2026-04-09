from django.urls import path

from booking import views

app_name = "booking"


urlpatterns = [
    path("", views.index, name="index"),
    path("my-bookings", views.my_bookings, name="my-bookings"),
    path("book/<str:desk_id>/<str:room_id>/<str:office_id>/", views.book, name="book"),
    path("book-delete/", views.book_delete, name="book-delete"),
]
