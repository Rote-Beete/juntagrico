from django.utils import timezone
from biddings.models import BiddingRound
from juntagrico.models import Member


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


class MemberMixin:
    def get_or_create_member(self, email, **kwargs):
        data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': email,
            'addr_street': 'addr_street',
            'addr_zipcode': '1234',
            'addr_location': 'addr_location',
            'phone': 'phone',
            'mobile_phone': 'phone',
            'confirmed': True,
        }
        data.update(kwargs)
        member, _ = Member.objects.get_or_create(defaults=data)
        return member
