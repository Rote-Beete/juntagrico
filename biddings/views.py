from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from biddings.models import Bid, BiddingRound

class ListBiddingroundView(LoginRequiredMixin, ListView):
    model = BiddingRound
    context_object_name = "bidding_rounds"

class CreateBidView(LoginRequiredMixin, CreateView):
    model = Bid
    fields = "__all__"

class UpdateBidView(LoginRequiredMixin, UpdateView):
    model = Bid
    fields = "__all__"


class DeleteBidView(LoginRequiredMixin, DeleteView):
    model = Bid