from django.contrib import admin
from biddings.models import Bid, BiddingRound
from juntagrico.entity.subs import Subscription
from django import forms
from django.utils.translation import gettext_lazy as _
from biddings.templatetags.biddings_extras import get_name

admin.site.register(BiddingRound)


class AdminBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        subs = list(Subscription.objects.all())
        subs_sorted = sorted(subs, key=get_name)
        self.fields["subscription"].choices = [(sub.id, sub) for sub in subs_sorted]
        self.fields["subscription"].label = _("Gemüseanteil")


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    form = AdminBidForm
