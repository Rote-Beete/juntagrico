from django.urls import path

from biddings.views import (
    ListBiddingroundView,
)

urlpatterns = [
    path('', ListBiddingroundView.as_view(), name='biddingrounds'),
]
