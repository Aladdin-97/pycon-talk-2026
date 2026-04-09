from django.contrib.auth import get_user_model
from django.db import models
from app_core.models import Desk, Office, Room


class Booking(models.Model):
    class Meta:
        # Ensure that a desk can only be booked once for a specific date
        constraints = [
            models.UniqueConstraint(fields=["desk", "booked_on"], name="unique_booking")
        ]

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.AutoField(primary_key=True)
    desk = models.ForeignKey(
        Desk, on_delete=models.CASCADE, related_name="booking_desk"
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, related_name="booking_user"
    )
    office = models.ForeignKey(
        Office, on_delete=models.CASCADE, related_name="booking_office", null=True
    )
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="booking_room", null=True
    )
    booked_on = models.DateField()
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        # Customize the string representation of the Booking object
        return f"Booking ID: {self.pk}, Booked On: {self.booked_on}, User: {self.user}, Office: {self.office}"

    def user_email(self):
        """Return the email of the user associated with the booking."""
        User = get_user_model()
        try:
            user = User.objects.get(pk=self.user_id)
            return [user.email]
        except User.DoesNotExist:
            # Handle the case when the user does not exist
            return []
        except AttributeError:
            # Handle the case when the user or email attribute is not available
            return []
