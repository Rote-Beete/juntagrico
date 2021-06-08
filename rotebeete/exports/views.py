import csv

from django.db.models import Count, Sum
from django.http import HttpResponse
from django.utils import timezone
from juntagrico.entity.depot import Depot
from juntagrico.entity.share import (
    reason_for_acquisition_choices,
    reason_for_cancellation_choices,
)
from juntagrico.models import Member

FIELDS = [
    "share__number",
    "first_name",
    "last_name",
    "addr_street",
    "addr_zipcode",
    "addr_location",
    "share__issue_date",
    "share__reason_for_acquisition",
    "share__count",
    "share__booking_date",
    "share__termination_date",
    "share__reason_for_cancellation",
    "share__creation_date",
]

ACQUISITION_REASONS = dict(reason_for_acquisition_choices)
CANCELLATION_REASONS = dict(reason_for_cancellation_choices)


def export_depot_list(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=Verteilstationen.csv"
    writer = csv.DictWriter(response, fieldnames=["name", "email"], dialect="unix")
    writer.writerow({"name": "Verteilstation", "email": "E-Mail-Adresse"})
    for depot in Depot.objects.order_by("name"):
        for member in Member.objects.filter(subscriptionmembership__subscription__depot=depot):
            row = dict(name=depot.name, email=member.email)
            writer.writerow(row)
    return response


def export_depot_overview(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=Verteilstationen.csv"
    writer = csv.DictWriter(response, fieldnames=["name", "sub_sum"], dialect="unix")
    writer.writerow({"name": "Verteilstation", "sub_sum": "Anteile"})
    for depot in Depot.objects.order_by("name"):
        row = dict(name=depot.name)
        row["sub_sum"], *_ = depot.subscription_set.aggregate(
            Sum("parts__type__size__units")
        ).values()
        writer.writerow(row)
    return response


def export_members(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=Mitglieder.csv"
    writer = csv.DictWriter(response, fieldnames=FIELDS, dialect="unix")
    writer.writerow(
        {
            "share__number": f"Mitgliederliste Gemüsekooperative Rote Beete eG (Stand: {timezone.now().date()})"
        }
    )
    writer.writerow({})
    writer.writerow(
        {
            "share__number": "GenoNr.",
            "first_name": "Mitgliederdaten",
            "share__issue_date": "Mitgliedschaft",
            "share__count": "weitere Geschäftsanteile (freiwillig)",
            "share__termination_date": "Ausscheiden",
            "share__creation_date": "Tag der Eintragung",
        }
    )
    writer.writerow(
        {
            "first_name": "Vorname",
            "last_name": "Name",
            "addr_street": "Straße",
            "addr_zipcode": "PLZ",
            "addr_location": "Wohnort",
            "share__issue_date": "Tag des Erwerbs",
            "share__reason_for_acquisition": "Grund des Erwerbs",
            "share__count": "Anzahl der weiteren Geschäftsanteile",
            "share__booking_date": "Tag der Zulassung",
            "share__termination_date": "Tag des Ausscheidens",
            "share__reason_for_cancellation": "Grund des Ausscheidens",
        }
    )
    for row in (
        Member.objects.annotate(Count("share"))
        .order_by("share__number")
        .values(*FIELDS)
    ):
        if row.get("share__count", 0) > 0:
            row["share__reason_for_acquisition"] = ACQUISITION_REASONS.get(
                row["share__reason_for_acquisition"], ""
            )
            row["share__reason_for_cancellation"] = ACQUISITION_REASONS.get(
                row["share__reason_for_cancellation"], ""
            )
            row["share__count"] = row.get("share__count") - 1
            writer.writerow(row)
    return response
