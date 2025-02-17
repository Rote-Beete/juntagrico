from django.utils import timezone
from biddings.models import BiddingRound


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
        bidding_round, _ = BiddingRound.objects.get_or_create(defaults=data)
        return bidding_round
