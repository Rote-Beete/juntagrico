from django.urls import path

from biddings.views import (
    CreateBidView,
    DeleteBidView,
    ListBiddingroundView,
    UpdateBidView,
    export_bidding_round,
    export_bidding_rounds,
    export_bidding_round_no_bids,
)

urlpatterns = [
    path("", ListBiddingroundView.as_view(), name="biddingrounds"),
    path(
        "<int:bidding_round_pk>/create-bid", CreateBidView.as_view(), name="create_bid"
    ),
    path("<int:pk>/update", UpdateBidView.as_view(), name="update_bid"),
    path("<int:pk>/delete", DeleteBidView.as_view(), name="delete_bid"),
    path("export-list", export_bidding_rounds, name="export-bidding-rounds"),
    path(
        "export/<int:bidding_round_pk>",
        export_bidding_round,
        name="export-bidding-round",
    ),
    path(
        "export-no-bids/<int:bidding_round_pk>",
        export_bidding_round_no_bids,
        name="export-bidding-round-no-bids",
    ),
]
