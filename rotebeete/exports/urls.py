from django.urls import path

from rotebeete.exports.views import export_members, export_depot_overview, export_depot_list, export_subscriptions, \
    export_depot_emails

urlpatterns = [
    path('my/export/depots', export_depot_overview, name='lists-depot-amountoverview'),
    path('my/export/depots', export_depot_overview, name='lists-depot-overview'),
    path('my/export/depots/emails', export_depot_emails, name='export-depot-emails'),
    path('my/export/depots/subscriptions', export_depot_list, name='lists-depotlist'),
    path('my/export/members', export_members, name='export-members'),
    path('my/export/subscriptions', export_subscriptions, name='export-subscriptions'),
]
