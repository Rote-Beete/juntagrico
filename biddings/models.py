from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from juntagrico.entity.subs import Subscription
from juntagrico.entity.subtypes import SubscriptionSize


class BiddingRound(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    start_time = models.DateTimeField(verbose_name=_("Startzeit"))
    end_time = models.DateTimeField(verbose_name=_("Endzeit"))
    guiding_value = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name=_("Richtwert"),
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-start_time"]

    @property
    def is_active(self):
        return self.start_time <= timezone.now() <= self.end_time

    @property
    def is_in_future(self):
        return self.start_time > timezone.now()

    def get_sum_of_subscription_sizes(self):
        return sum(bid.get_size() for bid in self.bids.all())

    def get_average_bid_amount(self, color):
        valid_colors = {
            "green": "green_contribution_amount",
            "yellow": "yellow_contribution_amount",
            "red": "red_contribution_amount",
        }

        if color not in valid_colors:
            raise ValueError("Invalid color. Choose 'green', 'yellow', or 'red'.")

        bids = self.bids.all()
        if not bids.exists():
            return 0

        total_amount = float(sum(getattr(bid, valid_colors[color]) for bid in bids))
        return round(total_amount / self.get_sum_of_subscription_sizes(), 2)

    def __str__(self):
        return f"Bietrunde({self.pk}): {self.name} {self.start_time} -- {self.end_time} ({'not ' if not self.is_active else ''}aktiv)"


class Bid(models.Model):
    bidding_round = models.ForeignKey(
        "BiddingRound",
        on_delete=models.CASCADE,
        related_name="bids",
        verbose_name=_("Bietrunde"),
    )

    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.PROTECT,
        related_name="bids",
        verbose_name=_("Gemüseanteil"),
    )

    green_contribution_amount = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name=_("Grünes Gebot (Komfortzone)")
    )
    yellow_contribution_amount = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name=_("Gelbes Gebot (Machbar)")
    )
    red_contribution_amount = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name=_("Rotes Gebot (Schmerzgrenze)")
    )

    subscription_size = models.ForeignKey(
        SubscriptionSize,
        on_delete=models.PROTECT,
        related_name='bid',
        verbose_name=_('Gewünschte Anzahl der Anteile'),
        null=True,
        blank=True,
    )

    comment = models.TextField(verbose_name=_("Kommentar"), null=True, blank=True)

    class Meta:
        ordering = [
            "-bidding_round__start_time",
            "subscription_id",
        ]

    def get_absolute_url(self):
        return reverse("biddingrounds")

    def get_primary_member(self):
        return self.subscription.primary_member

    def get_size(self):
        return sum(
            [part.type.size.units for part in self.subscription.active_and_future_parts]
        )

    def get_type_names(self):
        return ", ".join(
            [part.type.name for part in self.subscription.active_and_future_parts]
        )

    def __str__(self):
        return f"Gebot({self.pk}): {self.bidding_round.name} {self.bidding_round.start_time.date()} {self.subscription} {self.get_primary_member()}"
