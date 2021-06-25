import csv
import sys
from datetime import date

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError
from django.core.management.base import BaseCommand
from juntagrico.entity.subtypes import SubscriptionType
from juntagrico.models import Member, Share, Subscription, SubscriptionMembership


COLS = [
    "lfdnr",
    "genonr",      # ok
    "stand",       # teilweise
    "glv",         # ok
    "kontaktglv",  # ok
    "vorname",     # ok
    "name",        # ok
    "strasse",     # ok
    "plz",         # ok
    "ort",         # ok
    "mail",        # ok
    "fon",         # ok
    "erwerb",      # ok
    "grund",       # ok
    "datum_be",
    "ga_gesamt",   # ok
    "weitere_ga",
    "zulassung",   # ok
    "einlage",
    "einlagen",
    "betrag",
    "pruef",
    "aufnahme",
    "ausscheiden", # ok
    "grund_aus",   # ok
    "datenschutz",
    "kuendigung",  # ok
    "best_kuend",
    "eintragung",  # ok
    "anm1",
    "anm2",
    "anm3",
    "anm4",
    "ueberweisung",
    "konto",
    "bezahlt",     # ok
]


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("csv_file")

    def handle(self, *args, **options):
        with open(options["csv_file"], newline="") as f:
            reader = csv.DictReader(f, fieldnames=COLS)
            for row in reader:
                if row["genonr"].isdecimal():
                    self.import_row(row)
                else:
                    self.stdout.write(self.style.WARNING("Invalid Geno nr: {}".format(row["genonr"])))

    def import_row(self, row):
        member = self.get_member(row["genonr"], row["mail"])
        self.create_shares(member, row)
        self.create_subscription(member, row["glv"], row["kontaktglv"].strip() == "1")
        self.set_basic_data(member, row)
        self.clean(member)
        try:
            member.save()
        except AttributeError:
            self.stdout.write(self.style.WARNING("Could not save member: {}".format(member)))

    def get_member(self, genonr, mail) -> Member:
        if not mail or mail == "Null":
            mail = "invalid+{}@rotebeete.org".format(genonr)
        share = Share.objects.filter(number=genonr).first()
        if share:
            member = share.member
        else:
            member, _ = Member.objects.get_or_create(email=mail)
        return member

    def set_basic_data(self, member, row):
        member.first_name = row["vorname"]
        member.last_name = row["name"]
        member.phone = row["fon"]
        member.addr_street = row["strasse"]
        member.addr_zipcode = row["plz"]
        member.addr_location = row["ort"]
        member.confirmed = True
        if row["stand"].strip() == "99":
            date = self.get_date(row["ausscheiden"])
            if date is not None:
                member.deactivation_date = date
                member.end_date = date
                try:
                    member.save()
                except ValidationError:
                    member.deactivation_date = None
                    member.end_date = None
                    self.stdout.write(self.style.WARNING("Member has quit but still has shares: {}".format(member)))
                except AttributeError:
                    self.stdout.write(self.style.WARNING("Could not save member: {}".format(member)))
            else:
                self.stdout.write(self.style.WARNING("Invalid Tag des Ausscheidens for member {}".format(member)))
            date = self.get_date(row["kuendigung"])
            if date is not None:
                member.cancellation_date = date
            else:
                self.stdout.write(self.style.WARNING("Invalid Kündigungsdatum for member {}".format(member)))

    def create_shares(self, member, row):
        if row["ga_gesamt"].isdecimal():
            share_count = int(row["ga_gesamt"])
            if share_count > 0:
                while Share.objects.filter(member=member).count() < share_count:
                    share = Share.objects.create(member=member)
                    share.number = row["genonr"]
                    if row["grund"] == "GM":
                        share.reason_for_acquisition = 1
                    elif row["grund"] == "BE":
                        share.reason_for_acquisition = 2
                    else:
                        self.stdout.write(self.style.WARNING("Invalid Grund des Erwerbs: {}".format(row["grund"])))
                    share.save()
            try:
                for share in Share.objects.filter(member=member).all():
                    share.paid_date = self.get_date(row["bezahlt"])
                    share.issue_date = self.get_date(row["erwerb"])
                    share.booking_date = self.get_date(row["zulassung"])
                    share.creation_date = self.get_date(row["eintragung"])
                    if row["stand"].strip() == "99":
                        share.termination_date = self.get_date(row["ausscheiden"])
                        share.cancelled_date = self.get_date(row["kuendigung"])
                        if row["grund_aus"].strip() == "Kündigung":
                            share.reason_for_cancellation = 1
                        else:
                            self.stdout.write(
                                self.style.WARNING("Invalid Grund des Ausscheidens for member {}".format(member)))
                    share.save()
            except ValidationError:
                self.stdout.write(self.style.WARNING("Error when writing dates for member shares of {}".format(member)))
        else:
            self.stdout.write(self.style.WARNING(
                "Invalid GA gesamt: {} (member id {})".format(row["ga_gesamt"], member.id)))

    def get_date(self, date_str):
        try:
            if date_str.count(".") >= 2:
                dd, mm, yy, *_ = date_str.strip().split(".")
                if len(yy) == 4:
                    return date.fromisoformat(f"{yy}-{mm}-{dd}")
                else:
                    return date.fromisoformat(f"20{yy}-{mm}-{dd}")
        except ValueError:
            pass
        return None

    def clean(self, member):
        if not member.phone or member.phone == "Null" or member.phone == "-":
            member.phone = "unbekannt"
        if not member.addr_street or member.addr_street == "Null" or member.addr_street == "-":
            member.addr_street = "unbekannt"
        if not member.addr_zipcode or member.addr_zipcode == "Null" or member.addr_zipcode == "-":
            member.addr_zipcode = "unbekannt"
        if not member.addr_location or member.addr_location == "Null" or member.addr_location == "-":
            member.addr_location = "unbekannt"
        if member.mobile_phone and member.mobile_phone.startswith("genonr:"):
            member.mobile_phone = ""

    def create_subscription(self, member, glv, primary):
        if glv == "Null":
            return
        try:
            subtype = SubscriptionType.objects.get(name=glv)
            sub = Subscription.objects.get(parts__type=subtype)
            SubscriptionMembership.objects.get_or_create(member=member, subscription=sub)
            if primary:
                sub.primary_member = member
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            self.stdout.write(self.style.WARNING("Abo/Typ not yet existing: {} (member {})".format(glv, member)))
        except ValidationError:
            self.stdout.write(self.style.WARNING("Member already has another Abo: {}".format(member)))
