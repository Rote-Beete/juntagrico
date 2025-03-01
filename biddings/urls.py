from django.urls import path

from biddings.views import ListBiddingroundView, CreateBidView, DeleteBidView, UpdateBidView

urlpatterns = [
    path('', ListBiddingroundView.as_view(), name='biddingrounds'),
    path('<int:bidding_round_pk>/create-bid', CreateBidView.as_view(), name='create_bid'),
    path('<int:pk>/update', UpdateBidView.as_view(), name='update_bid'),
    path('<int:pk>/delete', DeleteBidView.as_view(), name='delete_bid'),
]
