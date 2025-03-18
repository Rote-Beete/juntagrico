from django.forms import ModelForm, ValidationError
from django.utils.translation import gettext_lazy as _
from biddings.models import Bid


class BidForm(ModelForm):
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


class BidCreateForm(BidForm):
    class Meta:
        model = Bid
        exclude = ["bidding_round", "subscription", "bidder"]


class BidUpdateForm(BidForm):
    class Meta:
        model = Bid
        exclude = ["bidding_round", "subscription", "bidder"]
