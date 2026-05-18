from django.test import TestCase
from biddings.tests.mixins import MemberMixin, SubscriptionMixin


class MemberMixinTestCase(MemberMixin, TestCase):
    def test_get_or_create_member(self):
        member = self.get_or_create_member(email="test@roko.li")
        assert member.email == "test@roko.li"


class SubscriptionMixinTestCase(SubscriptionMixin, TestCase):
    def test_get_or_create_depot(self):
        depot = self.get_or_create_depot()
        assert depot.name == "depot"

    def test_get_or_create_subscription_without_primary_member(self):
        subscription = self.get_or_create_subscription()
        assert subscription.primary_member is None

    def test_get_or_create_subscription_with_primary_member(self):
        subscription = self.get_or_create_subscription(
            primary_member=self.get_or_create_member(email="test@roko.li")
        )
        assert subscription.primary_member.email == "test@roko.li"
        assert (
            sum(
                [
                    product_size.units
                    for part in subscription.active_and_future_parts
                    for product_size in part.type.bundle.product_sizes.all()
                ]
            )
            == 5.5
        )
