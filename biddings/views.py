from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from biddings.models import BiddingRound


class ListBiddingroundView(LoginRequiredMixin, ListView):
    model = BiddingRound
    context_object_name = "bidding_rounds"
