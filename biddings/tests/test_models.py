from time import sleep
from django.test import TestCase
from django.utils import timezone
from biddings.tests.mixins import BiddingRoundMixin, SubscriptionMixin
from biddings.models import Bid


class BiddingRoundTestCase(BiddingRoundMixin, TestCase):
    def setUp(self):
        self.start_time = timezone.now()
        self.end_time = self.start_time + timezone.timedelta(days=6, hours=3)
        self.bidding_round = self.get_or_create_bidding_round(
            self.start_time, self.end_time
        )

    def test_create_bidding_round_with_valid_times(self):
        assert self.bidding_round.start_time, self.bidding_round.end_time == (
            self.start_time,
            self.end_time,
        )

    def test_is_active(self):
        assert self.bidding_round.is_active is True
        self.bidding_round.end_time = timezone.now()
        sleep(0.1)
        assert self.bidding_round.is_active is False


class BidTestCase(SubscriptionMixin, BiddingRoundMixin, TestCase):
    def setUp(self):
        self.primary_member = self.get_or_create_member(email="test@roko.li")
        self.subscription = self.get_or_create_subscription(
            primary_member=self.primary_member
        )
        self.bidding_round = self.get_or_create_bidding_round()
        self.data = {
            "bidding_round": self.bidding_round,
            "subscription": self.subscription,
            "green_contribution_amount": 10,
            "yellow_contribution_amount": 15,
            "red_contribution_amount": 20,
            "comment": "Some comments...",
        }

    def test_create_bid(self):
        bid, _ = Bid.objects.get_or_create(**self.data)

        for field_name, value in self.data.items():
            assert getattr(bid, field_name) == value

        assert bid.get_size() == 5.5

        assert bid.get_primary_member() == self.primary_member

    def test_get_all_members(self):
        member_1 = self.get_or_create_member(email="member1@roko.li", first_name="Mani", last_name="something")
        member_2 = self.get_or_create_member(email="member2@roko.li", first_name="Mona", last_name="Else")

        self.subscription.subscriptionmembership_set.create(member=member_1)
        self.subscription.subscriptionmembership_set.create(member=member_2)

        bid, _ = Bid.objects.get_or_create(defaults=self.data)
        assert bid.subscription.recipients == [self.primary_member, member_1, member_2]