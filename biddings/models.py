from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from juntagrico.models import Member


class BiddingRound(models.Model):
    start_time = models.DateTimeField(verbose_name=_("Bidding Start Time"))
    end_time = models.DateTimeField(verbose_name=_("Bidding End Time"))

    @property
    def is_active(self):
        return self.start_time <= timezone.now() <= self.end_time


class Bid(models.Model):
    bidding_round = models.ForeignKey(
        "BiddingRound",
        on_delete=models.CASCADE,
        related_name="bids",
        verbose_name=_("Bidding Round"),
    )
    participant = models.ForeignKey(
        Member,
        on_delete=models.PROTECT,
        related_name="bids",
        verbose_name=_("Bid's Participant"),
    )
    green_contribution_amount = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name=_("Green Contribution Amount")
    )
    yellow_contribution_amount = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name=_("Yellow Contribution Amount")
    )
    red_contribution_amount = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name=_("Red Contribution Amount")
    )
    number_of_shares = models.PositiveIntegerField(
        verbose_name=_("Bid's Number of Shares")
    )
    comment = models.TextField(verbose_name=_("Bid's Comment"))
