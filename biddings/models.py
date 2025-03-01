from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from juntagrico.models import Subscription


class BiddingRound(models.Model):
    start_time = models.DateTimeField(verbose_name=_("Bidding Start Time"))
    end_time = models.DateTimeField(verbose_name=_("Bidding End Time"))

    @property
    def is_active(self):
        return self.start_time <= timezone.now() <= self.end_time

    def __str__(self):
        return f"Bidding Round {self.start_time.date()} -- {self.end_time.date()} ({'not ' if not self.is_active else ''}active)"


class Bid(models.Model):
    bidding_round = models.ForeignKey(
        "BiddingRound",
        on_delete=models.CASCADE,
        related_name="bids",
        verbose_name=_("Bidding Round"),
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.PROTECT,
        related_name="bids",
        verbose_name=_("Subscription"),
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

    comment = models.TextField(verbose_name=_("Bid's Comment"))

    def get_number_of_shares(self):
        return sum(
            [part.type.size.units for part in self.subscription.active_and_future_parts]
        )

    def get_primary_member(self):
        return self.subscription.primary_member
