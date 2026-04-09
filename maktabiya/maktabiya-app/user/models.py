from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField()
    avatar = models.ImageField(upload_to="avatar", blank=True, null=True)
    # the desk booked owner is visible by others if this is set true
    booking_visible = models.BooleanField(
        default=True, blank=False, null=False, verbose_name="Booking Visibile By Others"
    )
    manager = models.ForeignKey(
        "Manager", on_delete=models.SET_NULL, blank=True, null=True
    )


# Manager model with additional fields
class Manager(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} {self.surname}"
