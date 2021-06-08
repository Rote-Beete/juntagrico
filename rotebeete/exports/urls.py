from django.urls import path

from rotebeete.exports.views import export_members, export_depot_overview, export_depot_list

urlpatterns = [
    path('my/export/members', export_members, name='export-members'),
    path('my/pdf/depotlist', export_depot_list, name='lists-depotlist'),
    path('my/pdf/depotoverview', export_depot_overview, name='lists-depot-overview'),
]
