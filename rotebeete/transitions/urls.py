from django.urls import path

from rotebeete.transitions.views import ReviewView

urlpatterns = [
    path("my/review", ReviewView.as_view(), name="review"),
    path(
        "my/review/confirm-data",
        ReviewView.as_view(),
        name="confirm-data-review",
    ),
    path(
        "my/review/confirm-membership",
        ReviewView.as_view(),
        name="confirm-membership-review",
    ),
]
