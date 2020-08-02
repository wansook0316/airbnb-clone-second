from django.db import models
from django.utils import timezone
from core import models as core_models


class Reservation(core_models.TimeStampedModel):
    """ Reservation Model Definition """

    # 이 부분을 abstract model(Room model에서 한것 처럼)을 만들어서 할 수 있지만,
    # 방 예약 상태는 고정되있으므로 그냥 하드코딩으로 만드는 것도 괜찮다.
    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f"{self.room} - {self.check_in}"

    def in_progress(self):
        now = timezone.now().date()
        return self.check_in <= now and now < self.check_out

    def is_finished(self):
        now = timezone.now().date()
        return self.check_out < now

    in_progress.boolean = True  # 장고 admin에서 사용하는 예쁜 boolean icon을 사용가능하다.
    is_finished.boolean = True
