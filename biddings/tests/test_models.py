from time import sleep
from django.test import TestCase

from biddings.models import BiddingRound
from django.utils import timezone


class BiddingRoundTestCase(TestCase):
    def setUp(self):
        self.start_time = timezone.now()
        self.end_time = self.start_time + timezone.timedelta(days=6, hours=3)
        self.bidding_round = BiddingRound.objects.create(
            start_time=self.start_time, end_time=self.end_time
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
