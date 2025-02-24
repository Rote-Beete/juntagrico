from django.urls import path

from biddings.views import biddinground_list


urlpatterns = [
    path('', biddinground_list, name='biddingrounds'),
]
