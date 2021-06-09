from django.urls import path

from rotebeete.exports.views import export_members, export_depot_overview, export_depot_list, export_subscriptions

urlpatterns = [
    path('my/export/members', export_members, name='export-members'),
    path('my/export/subscriptions', export_subscriptions, name='export-subscriptions'),
    path('my/pdf/depotlist', export_depot_list, name='lists-depotlist'),
    path('my/pdf/depotoverview', export_depot_overview, name='lists-depot-overview'),
]
