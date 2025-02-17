from time import sleep
from django.test import TestCase
from django.utils import timezone
from biddings.tests.mixins import BiddingRoundMixin, MemberMixin


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


class BidTestCase(MemberMixin, BiddingRoundMixin, TestCase):
    def setUp(self):
        self.participant = self.get_or_create_member(email="test@roko.li")
        self.bidding_round = self.get_or_create_bidding_round()

    def test_create_bid(self):
        bid = Bid.objects.create(
            bidding_round=self.bidding_round,
            participant=self.participant,
            green_contribution_amount=10,
            yello_contribution_amount=15,
            red_contribution_amount=20,
            number_of_shares=3,
            comment="Some comments...",
        )
