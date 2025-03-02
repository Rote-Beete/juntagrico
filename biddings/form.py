from django.forms import ModelForm
from juntagrico.models import Subscription

from biddings.models import Bid


class BidCreateForm(ModelForm):
    class Meta:
        model = Bid
        exclude = ["bidding_round"]

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subscription"].queryset = Subscription.objects.filter(
            primary_member__user=user
        )


class BidUpdateForm(ModelForm):
    class Meta:
        model = Bid
        exclude = ["bidding_round", "subscription"]
