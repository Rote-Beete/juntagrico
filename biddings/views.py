import csv
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.http import HttpResponse
from biddings.form import BidUpdateForm
from biddings.models import Bid, BiddingRound
from juntagrico.entity.subtypes import SubscriptionType

from biddings.templatetags.biddings_extras import get_user_subscription


class ListBiddingroundView(LoginRequiredMixin, ListView):
    model = BiddingRound
    context_object_name = "bidding_rounds"


class _UserSubscriptionMixin:
    def _get_subscription(self):
        # Juntagrico allows a member to have multiple subscriptions but rote beete is using at the moment only one subscription per member.
        return get_user_subscription(self.request.user)

    def _get_subscription_size(self):
        try:
            return SubscriptionType.objects.filter(
                subscription_parts__in=self._get_subscription().active_and_future_parts
            )[0].size
        except (IndexError, AttributeError):
            return None


class CreateBidView(LoginRequiredMixin, CreateView, _UserSubscriptionMixin):
    model = Bid
    form_class = BidUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bidding_round"] = BiddingRound.objects.get(
            pk=self.kwargs["bidding_round_pk"]
        )
        context["subscription"] = self._get_subscription()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'initial': {'subscription_size': self._get_subscription_size()}})
        return kwargs

    def form_valid(self, form):
        bidding_round = get_object_or_404(
            BiddingRound, pk=self.kwargs["bidding_round_pk"]
        )
        form.instance.bidding_round = bidding_round
        form.instance.subscription = self._get_subscription()
        return super().form_valid(form)


class UpdateBidView(
    LoginRequiredMixin, UserPassesTestMixin, UpdateView, _UserSubscriptionMixin
):
    model = Bid
    form_class = BidUpdateForm

    def test_func(self):
        return (
            self.request.user.member in self.get_object().subscription.current_members
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bidding_round"] = self.get_object().bidding_round
        context["subscription"] = self._get_subscription()
        return context


class DeleteBidView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Bid
    success_url = reverse_lazy("biddingrounds")

    def test_func(self):
        return (
            self.request.user.member in self.get_object().subscription.current_members
        )


@login_required
def export_bidding_rounds(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    return render(
        request,
        "biddings/biddinground_export_list.html",
        context={"bidding_rounds": BiddingRound.objects.all()},
    )


@login_required
def export_bidding_round(request, bidding_round_pk):
    if not request.user.is_superuser:
        raise PermissionDenied
    bidding_round = get_object_or_404(BiddingRound, pk=bidding_round_pk)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f"attachment; filename=Bietrunde {bidding_round.name} {bidding_round.start_time.date()} {bidding_round.end_time.date()}.csv"
    )
    writer = csv.DictWriter(
        response,
        fieldnames=[
            "subscprition_type_names",
            "primary_member",
            "subscription_size",
            "green_bid",
            "yellow_bid",
            "red_bid",
            "comment",
        ],
        dialect="unix",
    )
    writer.writerow(
        {
            "subscprition_type_names": "GVL-Nr.",
            "primary_member": "Hauptbezieher*in",
            "subscription_size": "Anzahl Anteile",
            "green_bid": "Grünes Gebot",
            "yellow_bid": "Gelbes Gebot",
            "red_bid": "Rotes Gebot",
            "comment": "Kommentar",
        }
    )
    latest_bids = Bid.objects.latest_per_subscription_in_round(bidding_round)
    for bid in latest_bids:
        row = dict(
            subscprition_type_names=bid.get_type_names(),
            primary_member=bid.get_primary_member(),
            subscription_size=bid.get_size(),
            green_bid=bid.green_contribution_amount,
            yellow_bid=bid.yellow_contribution_amount,
            red_bid=bid.red_contribution_amount,
            comment=bid.comment,
        )
        writer.writerow(row)

    writer.writerow(
        {
            "subscprition_type_names": "",
            "primary_member": "",
            "subscription_size": f"Summe: {bidding_round.get_sum_of_subscription_sizes()}",
            "green_bid": f"Durchschnitt: {bidding_round.get_average_bid_amount('green')}",
            "yellow_bid": f"Durchschnitt: {bidding_round.get_average_bid_amount('yellow')}",
            "red_bid": f"Durchschnitt: {bidding_round.get_average_bid_amount('red')}",
            "comment": "",
        }
    )

    return response
