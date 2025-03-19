from django import template

from biddings.models import Bid
from juntagrico.entity.subtypes import SubscriptionType
from django.db.models import F, Sum

register = template.Library()


@register.filter
def get_bids(bidding_round, user):
    return Bid.objects.filter(bidding_round=bidding_round, bidder__user=user)


@register.filter
def get_name(subscription):
    delimiter = '|'
    sformat = 'GLV-Nr.: {name} / Anzahl Anteile: {amount}'
    types = SubscriptionType.objects.filter(
        subscription_parts__in=subscription.active_and_future_parts
    ).annotate(
        size_sum=Sum('size__units'),
        size_name=F('size__name'),
        product_name=F('size__product__name'),
    )
    return delimiter.join(
        [
            sformat.format(
                name=t.name,
                amount=t.size_sum,
            )
            for t in types
        ]
    )
