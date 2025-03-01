from django import template

from biddings.models import Bid

register = template.Library()


@register.filter
def get_bids(bidding_round, user):
    return Bid.objects.filter(
        bidding_round=bidding_round, subscription__primary_member__user=user
    )
