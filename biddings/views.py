import csv
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from juntagrico.models import Subscription
from django.http import HttpResponse
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
            if Subscription.objects.filter(primary_member__user=self.request.user)
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
        kwargs["user"] = self.request.user
        return kwargs


class UpdateBidView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Bid
    form_class = BidUpdateForm
    template_name = "biddings/bid_update_form.html"

    def test_func(self):
        return self.get_object().subscription.primary_member.user == self.request.user


class DeleteBidView(LoginRequiredMixin, DeleteView):
    model = Bid
    success_url = reverse_lazy("biddingrounds")


@login_required
def export_bidding_rounds(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    return render(
        request,
        "biddings/biddinground_export_list.html",
        context={"biddingrounds": BiddingRound.objects.all()},
    )


@login_required
def export_bidding_round(request, bidding_round_pk):
    if not request.user.is_superuser:
        raise PermissionDenied
    bidding_round = get_object_or_404(BiddingRound, pk=bidding_round_pk)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f"attachment; filename=Bietrunde {bidding_round.start_time.date()} {bidding_round.end_time.date()}.csv"
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
    for bid in bidding_round.bids.all():
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

    return response
