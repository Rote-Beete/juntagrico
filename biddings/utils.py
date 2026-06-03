from decimal import Decimal

from django.db.models import Sum


def subscription_type_units(subscription_type):
    # Supports both v2 SubscriptionType (bundle/product_sizes) and ProductSize instances.
    if hasattr(subscription_type, "units"):
        return Decimal(str(subscription_type.units or 0))

    units = (
        subscription_type.bundle.product_sizes.aggregate(units=Sum("units"))["units"]
        or 0
    )
    return Decimal(str(units))
