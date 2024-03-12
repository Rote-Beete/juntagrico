from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView


class ReviewView(TemplateView):
    template_name = "transitions/review.html"

    def post(self, request: HttpRequest, *args, **kwargs):
        if request.path == reverse("confirm-data-review"):
            request.user.member.transition.data_needs_review = False
        if request.path == reverse("confirm-membership-review"):
            request.user.member.transition.membership_needs_review = False
        request.user.member.transition.save()
        return redirect("review")
