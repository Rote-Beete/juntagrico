from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from juntagrico.models import Subscription

from biddings.form import BidCreateForm, BidUpdateForm
from biddings.models import Bid, BiddingRound


class ListBiddingroundView(LoginRequiredMixin, ListView):
    model = BiddingRound
    context_object_name = "bidding_rounds"


class CreateBidView(LoginRequiredMixin, CreateView):
    model = Bid
    form_class = BidCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bidding_round"] = BiddingRound.objects.get(
            pk=self.kwargs["bidding_round_pk"]
        )
        context["user_has_subscriptions"] = (
            True
            if Subscription.objects.filter(
                primary_member__user=self.request.user, bid=None
            )
            else False
        )
        return context

    def form_valid(self, form):
        bidding_round = get_object_or_404(
            BiddingRound, pk=self.kwargs["bidding_round_pk"]
        )
        form.instance.bidding_round = bidding_round
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class UpdateBidView(LoginRequiredMixin, UpdateView):
    model = Bid
    form_class = BidUpdateForm
    template_name = "biddings/bid_update_form.html"


class DeleteBidView(LoginRequiredMixin, DeleteView):
    model = Bid
    success_url = reverse_lazy("biddingrounds")
