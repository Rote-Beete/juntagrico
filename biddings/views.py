from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def biddinground_list(request):
    return render(request, "biddings/biddinground_list.html", context={})
