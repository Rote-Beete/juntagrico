from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from biddings.models import BiddingRound


@login_required
def biddinground_list(request):
    context = {"biddingrounds": BiddingRound.objects.all()}
    return render(request, "biddings/biddinground_list.html", context=context)
