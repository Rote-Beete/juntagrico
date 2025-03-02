from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from biddings.form import BidForm
from biddings.models import Bid, BiddingRound


class ListBiddingroundView(LoginRequiredMixin, ListView):
    model = BiddingRound
    context_object_name = "bidding_rounds"


class CreateBidView(LoginRequiredMixin, CreateView):
    model = Bid
    form_class = BidForm

    def form_valid(self, form):
        bidding_round = get_object_or_404(
            BiddingRound, pk=self.kwargs["bidding_round_pk"]
        )
        form.instance.bidding_round = bidding_round
        return super().form_valid(form)


class UpdateBidView(LoginRequiredMixin, UpdateView):
    model = Bid
    form_class = BidForm

    def form_valid(self, form):
        bidding_round = get_object_or_404(BiddingRound, pk=self.kwargs["pk"])
        form.instance.bidding_round = bidding_round
        return super().form_valid(form)


class DeleteBidView(LoginRequiredMixin, DeleteView):
    model = Bid
