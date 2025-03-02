from django.forms import ModelForm

from biddings.models import Bid


class BidForm(ModelForm):
    class Meta:
        model = Bid
        exclude = ["bidding_round"]
