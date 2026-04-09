from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import logging

log = logging.getLogger(f"{settings.APP_LOGGER}.{__name__}")
ERR_TEMPLATE = "An exception of type {0} occurred. Arguments:\n{1!r}"


class Office(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name=_("Office Name"))

    def __str__(self):
        return self.name


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name=_("Room Name"))
    no_of_desk = models.SmallIntegerField(default=0, verbose_name=_("Number of Desks"))
    office = models.ForeignKey(
        Office,
        on_delete=models.CASCADE,
        related_name="rooms",
        verbose_name=_("Office Name"),
    )

    def __str__(self) -> str:
        return self.name

    @property
    def desk_available(self):
        return self.no_of_desk - self.desks.count()


class Desk(models.Model):
    # has_error = False
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="desks",
        verbose_name=_("Room Name"),
    )
    name = models.CharField(max_length=50, verbose_name=_("Desk Name"))

    class Meta:
        ordering = ["-room__name"]

    def __str__(self):
        return self.name

    @property
    def office_name(self):
        return self.room.office.name if self.room and self.room.office else None


class Setting(models.Model):
    bookings_per_day = models.PositiveIntegerField(default=0)
    bookings_per_user_per_week = models.PositiveIntegerField(default=0)

    @property
    def name(self):
        return "Booking Settings"
