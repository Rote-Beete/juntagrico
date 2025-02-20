from django.contrib import admin
from biddings.models import Bid, BiddingRound

admin.site.register(BiddingRound)
admin.site.register(Bid)
