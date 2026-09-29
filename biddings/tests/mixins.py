from django.utils import timezone
from django.urls import reverse
from juntagrico.entity.subtypes import (
    ProductSize,
    SubscriptionBundle,
    SubscriptionProduct,
    SubscriptionType,
)
from biddings.models import BiddingRound
from juntagrico.models import Member, Subscription
from juntagrico.entity.depot import Depot
from juntagrico.entity.location import Location


class BiddingRoundMixin:
    def get_or_create_bidding_round(
        self, start_time=None, end_time=None, **kwargs
    ) -> BiddingRound:
        if not start_time:
            start_time = timezone.now()
        if not end_time:
            end_time = start_time + timezone.timedelta(days=6, hours=3)

        data = {
            "start_time": start_time,
            "end_time": end_time,
        }

        data.update(kwargs)
        bidding_round, _ = BiddingRound.objects.get_or_create(**data)
        return bidding_round


class MemberMixin:
    def get_or_create_member(
        self, email="test@roko.li", first_name="John", last_name="Tester", **kwargs
    ):
        defaults = {
            'first_name': first_name,
            'last_name': last_name,
            'addr_street': 'addr_street',
            'addr_zipcode': '1234',
            'addr_location': 'addr_location',
            'phone': 'phone',
            'mobile_phone': 'phone',
            'confirmed': True,
        }
        defaults.update(kwargs)
        member, _ = Member.objects.get_or_create(email=email, defaults=defaults)
        return member


class SubscriptionMixin(MemberMixin):
    def get_or_create_location(self, **kwargs):
        data = {
            'name': "location",
            'latitude': '12.513',
            'longitude': '1.314',
            'addr_street': 'Fakestreet 123',
            'addr_zipcode': '1000',
            'addr_location': 'Faketown',
            'description': 'Place to be',
        }
        data.update(kwargs)
        location, _ = Location.objects.get_or_create(**data)
        return location

    def get_or_create_depot(self, **kwargs):
        data = {
            'name': 'depot',
            'weekday': 1,
            'location': self.get_or_create_location(),
        }
        data.update(kwargs)
        depot, _ = Depot.objects.get_or_create(**data)
        return depot

    def get_or_create_subscription(self, primary_member=None, **kwargs):
        data = {
            'depot': self.get_or_create_depot(),
            'start_date': '2017-01-01',
        }
        data.update(kwargs)
        subcription, _ = Subscription.objects.get_or_create(**data)

        product_1 = SubscriptionProduct.objects.create(name="Product 1")
        product_2 = SubscriptionProduct.objects.create(name="Product 2")
        size_1 = ProductSize.objects.create(
            name="Size 1",
            units=3.5,
            product=product_1,
        )
        size_2 = ProductSize.objects.create(
            name="Size 2",
            units=2,
            product=product_2,
        )

        bundle_1 = SubscriptionBundle.objects.create(long_name="Bundle 1")
        bundle_1.product_sizes.add(size_1)
        bundle_2 = SubscriptionBundle.objects.create(long_name="Bundle 2")
        bundle_2.product_sizes.add(size_2)

        subcription.parts.create(
            type=SubscriptionType.objects.create(
                name="Type 1",
                required_assignments=3,
                price=10,
                bundle=bundle_1,
            )
        )

        subcription.parts.create(
            type=SubscriptionType.objects.create(
                name="Type 2",
                required_assignments=2,
                price=12,
                bundle=bundle_2,
            )
        )

        subcription.primary_member = primary_member
        if primary_member:
            subcription.subscriptionmembership_set.create(member=primary_member)

        return subcription


class ViewPermissionsMixin:
    def check_login_required(self, url, method="get"):
        if method == "get":
            response = self.client.get(url)
        elif method == "post":
            response = self.client.post(url)
        else:
            raise ValueError
        assert response.status_code == 302
        assert response["Location"] == f"{reverse('login')}?next={url}"
