from django import forms
from django.forms import ModelForm, ModelChoiceField, ValidationError, Select
from django.utils.translation import gettext_lazy as _

from juntagrico.entity.subtypes import SubscriptionBundle
from biddings.models import Bid


class SubscriptionSizeSelect(Select):
    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        if value:
            bundle = SubscriptionBundle.objects.prefetch_related("product_sizes").get(
                id=str(value)
            )
            option["attrs"]["data-units"] = sum(
                bundle.product_sizes.values_list("units", flat=True)
            )

        return option


class BidUpdateForm(ModelForm):
    def clean(self):
        cleaned_data = self.cleaned_data
        green, yellow, red = [
            cleaned_data.get(key)
            for key in [
                "green_contribution_amount",
                "yellow_contribution_amount",
                "red_contribution_amount",
            ]
        ]
        if None not in [green, yellow, red]:
            if green < 0 or yellow < 0 or red < 0:
                raise ValidationError(_("Negative Beitrgashöhen sind nicht zulässig."))
            if not (green < yellow < red):
                raise ValidationError(_("Falsche Reihenfolge der Beitragshöhen"))
        return cleaned_data

    class Meta:
        model = Bid
        exclude = ["bidding_round", "subscription"]
        widgets = {
            "green_contribution_amount": forms.NumberInput(attrs={"min": 0}),
            "yellow_contribution_amount": forms.NumberInput(attrs={"min": 0}),
            "red_contribution_amount": forms.NumberInput(attrs={"min": 0}),
        }

    subscription_bundle = ModelChoiceField(
        queryset=SubscriptionBundle.objects.order_by("sort_order"),
        label=Bid._meta.get_field("subscription_bundle").verbose_name,
        widget=SubscriptionSizeSelect,
    )
