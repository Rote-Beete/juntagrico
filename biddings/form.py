from django.forms import ModelForm, ModelChoiceField, ValidationError
from django.utils.translation import gettext_lazy as _
from juntagrico.admin import SubscriptionSize
from biddings.models import Bid


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

    subscription_size = ModelChoiceField(
        queryset=SubscriptionSize.objects.order_by('units'),
        label=Bid._meta.get_field("subscription_size").verbose_name,
    )
