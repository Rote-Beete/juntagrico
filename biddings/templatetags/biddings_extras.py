from django import template

from biddings.models import Bid
from juntagrico.entity.subtypes import SubscriptionType
from django.db.models import F, Sum

register = template.Library()


def get_user_subscription(user):
    try:
        return user.member.subscriptionmembership_set.first().subscription
    except AttributeError:
        return None


@register.filter
def get_bid(bidding_round, user):
    # Juntagrico allows a member to have multiple subscriptions but rote beete is using at the moment only one subscription per member. For now we are We are only
    subscription = get_user_subscription(user)
    try:
        return Bid.objects.get(bidding_round=bidding_round, subscription=subscription)
    except Bid.DoesNotExist:
        return None


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
