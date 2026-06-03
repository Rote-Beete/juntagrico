from django.urls import path

from rotebeete.exports.views import (
    export_members,
    export_depot_overview,
    export_depot_list,
    export_subscriptions,
    export_depot_emails,
    export,
)

urlpatterns = [
    path('rb/export', export, name='export'),
    path('rb/export/depots', export_depot_overview, name='lists-depot-amountoverview'),
    path('rb/export/depots/emails', export_depot_emails, name='lists-depot-overview'),
    path('rb/export/depots/subscriptions', export_depot_list, name='lists-depotlist'),
    path('rb/export/members', export_members, name='export-members'),
    path('rb/export/subscriptions', export_subscriptions, name='export-subscriptions'),
]
