from django.contrib import admin
from biddings.models import Bid, BiddingRound
from juntagrico.entity.subs import Subscription
from juntagrico.admins.subscription_admin import SubscriptionAdmin

admin.site.register(BiddingRound)


class BiddingSubscriptionAdmin(SubscriptionAdmin):
    search_fields = [
        *SubscriptionAdmin.search_fields,
        "types__name",
        "types__long_name",
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by("types__name", "pk").distinct()

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        return queryset.order_by("types__name", "pk").distinct(), True


try:
    admin.site.unregister(Subscription)
except admin.sites.NotRegistered:
    pass

admin.site.register(Subscription, BiddingSubscriptionAdmin)


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    autocomplete_fields = ["subscription"]
