import datetime
from django.test import TestCase

from biddings.models import BiddingRound


class BiddingRoundTestCase(TestCase):
     def setUp(self):
         self.start_time = datetime.datetime.now()
         self.end_time = self.start_time + datetime.timedelta(days=6, hours=3)
     
     def test_create_bidding_round_with_valid_times(self):
        bidding_round = BiddingRound.objects.create(start_time=self.start_time, end_time=self.end_time)
        assert bidding_round.start_time, bidding_round.end_time == (self.start_time, self.end_time)
