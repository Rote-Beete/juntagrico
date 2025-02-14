from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class BiddingRound(models.Model):
    start_time = models.DateTimeField(_("Bidding Start Time"))
    end_time = models.DateTimeField(_("Bidding End Time"))

    @property
    def is_active(self):
        return self.start_time <= timezone.now() <= self.end_time
