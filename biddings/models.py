from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from juntagrico.models import Subscription


class BiddingRound(models.Model):
    start_time = models.DateTimeField(verbose_name=_("Startzeit"))
    end_time = models.DateTimeField(verbose_name=_("Endzeit"))

    class Meta:
        ordering = ["-start_time"]

    @property
    def is_active(self):
        return self.start_time <= timezone.now() <= self.end_time

    @property
    def is_in_future(self):
        return self.start_time > timezone.now()

    def __str__(self):
        return f"Beitragsrunde({self.pk}): {self.start_time} -- {self.end_time} ({'not ' if not self.is_active else ''}aktiv)"


class Bid(models.Model):
    bidding_round = models.ForeignKey(
        "BiddingRound",
        on_delete=models.CASCADE,
        related_name="bids",
        verbose_name=_("Beitragsrunde"),
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.PROTECT,
        related_name="bids",
        verbose_name=_("Gemüseanteil"),
    )
    green_contribution_amount = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name=_("Grünes Gebot")
    )
    yellow_contribution_amount = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name=_("Gelbes Gebot")
    )
    red_contribution_amount = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name=_("Rotes Gebot")
    )

    comment = models.TextField(verbose_name=_("Kommentar"), null=True, blank=True)

    class Meta:
        ordering = [
            "-bidding_round__start_time",
            "subscription__primary_member__first_name",
        ]

    def get_number_of_shares(self):
        return sum(
            [part.type.size.units for part in self.subscription.active_and_future_parts]
        )

    def get_primary_member(self):
        return self.subscription.primary_member

    def get_absolute_url(self):
        return reverse("biddingrounds")

    def __str__(self):
        return f"Gebot({self.pk}): {self.bidding_round.start_time.date()} {self.subscription} {self.get_primary_member()}"
