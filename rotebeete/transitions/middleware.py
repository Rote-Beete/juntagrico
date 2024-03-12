from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse

DENIED_URL_PATHS = [
    reverse("areas"),
    reverse("contact"),
    reverse("deliveries"),
    reverse("home"),
    reverse("jobs"),
]


class ReviewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        try:
            transition = request.user.member.transition
            if (
                (transition.data_needs_review or transition.membership_needs_review)
                and request.path in DENIED_URL_PATHS
                and request.path != reverse("review")
            ):
                return redirect("review")
        except AttributeError:
            pass
        return self.get_response(request)
