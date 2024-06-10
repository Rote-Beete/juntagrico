from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.utils.translation import gettext as _
from juntagrico.util import temporal

from rotebeete.util.pdf import render_to_pdf_http


class ReviewView(TemplateView):
    template_name = "transitions/review.html"

    def post(self, request: HttpRequest, *args, **kwargs):
        if request.path == reverse("confirm-data-review"):
            request.user.member.transition.data_needs_review = False
        if request.path == reverse("confirm-membership-review"):
            request.user.member.transition.membership_needs_review = False
        request.user.member.transition.save()
        return redirect("review")


class DownloadDeliveryContract(View):
    def get(self, request: HttpRequest):
        member = request.user.member
        subscription = member.subscription_current
        share = member.active_shares.first()
        subtype = subscription.active_parts.first().type
        share_amount = subtype.size.units
        depot = subscription.depot.name
        season_years = f"{temporal.start_of_business_year().year}/{temporal.end_of_business_year().year}"
        context = {
            "member": member,
            "geno_number": share.number if share else "-",
            "depot": depot,
            "share_amount": share_amount,
            "subscription": subscription,
            "co_members": subscription.co_members(member),
            "glv_number": subtype.name,
            "business_year": {
                "date_start": temporal.start_of_business_year(),
                "date_end": temporal.end_of_business_year(),
                "years": season_years,
            },
            "monthly_fee": subtype.price,
        }
        if request.GET.get("debug_html", False):
            return render(
                request, "transitions/vegetable_delivery_contract.html", context
            )
        return render_to_pdf_http(
            "transitions/vegetable_delivery_contract.html",
            context,
            _("Gemüseliefervertrag") + ".pdf",
        )
