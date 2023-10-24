import csv
from datetime import date
from decimal import Decimal

from django.db.models import Count, Sum, Q
from django.http import HttpResponse
from django.utils import timezone
from juntagrico.entity.depot import Depot
from juntagrico.entity.share import (
    reason_for_acquisition_choices,
    reason_for_cancellation_choices,
    Share,
)
from juntagrico.entity.subs import Subscription
from juntagrico.entity.subtypes import SubscriptionType
from juntagrico.models import Member
from juntagrico.util.models import q_isactive

FIELDS = [
    "share__number",
    "first_name",
    "last_name",
    "email",
    "phone",
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


def get_status(sub: Subscription) -> str:
    status = "undefiniert"
    today = timezone.now().date()
    if sub.deactivation_date and sub.deactivation_date <= today:
        status = "beendet"
    elif sub.end_date and sub.end_date >= today:
        status = "gekündigt"
    elif sub.start_date and sub.start_date > today:
        status = "wartend"
    elif sub.activation_date and sub.activation_date <= today:
        status = "aktiv"
    return status


def export_subscriptions(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=Gemüseanteile_Übersicht.csv"
    writer = csv.DictWriter(response, dialect="unix", fieldnames=[
        "glv",
        "geno",
        "glv-eingang",
        "primary",
        "mail",
        "tel",
        "mobile",
        "status",
        "iban",
        "vs",
        "size",
        "price_per_unit",
        "price",
    ])
    writer.writerow({
        "glv": "GLV-Nr.",
        "geno": "Geno-Nr.",
        "glv-eingang": "GLV-Eingang",
        "primary": "HauptbezieherIn",
        "mail": "HauptbezieherInEmail",
        "tel": "HauptbezieherInTelefon",
        "mobile": "HauptbezieherInMobile",
        "status": "Status",
        "iban": "IBAN",
        "vs": "Verteilstation",
        "size": "Anteil/e",
        "price_per_unit": "Preis Pro Anteil",
        "price": "Preis",
    })
    sum_units = 0
    sum_price = 0
    for subtype in SubscriptionType.objects.order_by("name"):
        for part in subtype.subscription_parts.all():
            sub = part.subscription
            member = sub.primary_member
            share = member.share_set.first() if member else None
            writer.writerow({
                "glv": subtype.name,
                "geno": share.number if share else "",
                "glv-eingang": "",
                "primary": f"{member.last_name}, {member.first_name}" if member else "",
                "mail": member.email if member else "",
                "tel": member.phone if member else "",
                "mobile": member.mobile_phone if member else "",
                "status": get_status(sub),
                "iban": member.iban if member else "",
                "vs": sub.depot.name,
                "size": subtype.size.units,
                "price_per_unit": subtype.price / Decimal(subtype.size.units),
                "price": subtype.price,
            })
            sum_units += subtype.size.units
            sum_price += subtype.price
    writer.writerow({
        "size": sum_units,
        "price": sum_price,
        "price_per_unit": sum_price / Decimal(sum_units),
    })
    return response


def export_depot_emails(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=VS_eMail_Listen.csv"
    writer = csv.DictWriter(response, fieldnames=["name", "email"], dialect="unix")
    writer.writerow({"name": "Verteilstation", "email": "E-Mail-Adresse"})
    for depot in Depot.objects.order_by("name"):
        for sub in Subscription.objects.filter(q_isactive(), depot=depot):
            for membership in sub.subscriptionmembership_set.filter(Q(leave_date__isnull=True) | Q(leave_date__gte=date.today())):
                row = dict(name=depot.name, email=membership.member.email)
                writer.writerow(row)
    return response


def export_depot_list(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=VS_Listen.csv"
    writer = csv.DictWriter(response, fieldnames=["depot", "glv", "name", "units"], dialect="unix")
    writer.writerow({
        "depot": "Verteilstation",
        "glv": "GLV-Nr.",
        "name": "Gruppenbezeichnung / Name",
        "units": "Anteil/e"
    })
    for depot in Depot.objects.order_by("name"):
        for sub in Subscription.objects.filter(q_isactive(), depot=depot):
            for part in sub.parts.all():
                row = dict(
                    depot=depot.name,
                    glv=part.type.name,
                    name=sub.nickname if sub.nickname else sub.primary_member,
                    units=part.type.size.units,
                )
                writer.writerow(row)
    return response


def export_depot_overview(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=Mengen_Übersicht_VS.csv"
    writer = csv.DictWriter(response, fieldnames=["name", "sub_sum"], dialect="unix")
    writer.writerow({"name": "Verteilstation", "sub_sum": "Anteile"})
    for depot in Depot.objects.order_by("name"):
        row = dict(name=depot.name)
        row["sub_sum"], *_ = depot.subscription_set.filter(q_isactive()).aggregate(
            Sum("parts__type__size__units")
        ).values()
        writer.writerow(row)
    return response


def export_members(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=Mitgliederliste_Genossenschaft.csv"
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
            "email": "E-Mail-Adresse",
            "phone": "Telefonnummer",
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
    row_fields = FIELDS[:]
    row_fields.remove("share__count")
    for row in (
        Member.objects
        .order_by("share__number", "share__creation_date")
        .distinct("share__number")
        .values(*row_fields)
    ):
        row["share__count"] = Share.objects.filter(number=row["share__number"]).count()
        if row.get("share__count", 0) > 0:
            row["share__reason_for_acquisition"] = ACQUISITION_REASONS.get(
                row["share__reason_for_acquisition"], ""
            )
            row["share__reason_for_cancellation"] = CANCELLATION_REASONS.get(
                row["share__reason_for_cancellation"], ""
            )
            row["share__count"] = row.get("share__count") - 1
            writer.writerow(row)
    return response
