import csv
import sys
from datetime import date

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from juntagrico.entity.depot import Depot
from juntagrico.entity.subtypes import SubscriptionSize, SubscriptionType
from juntagrico.models import Share, Subscription, SubscriptionMembership


COLS = [
    "glv",         # ok
    "geno",        # ok
    "status",
    "glv2",
    "statut",
    "datenschutz",
    "nick",        # ok
    "mail",
    "vsnr",        # ok
    "anteile",     # ok
    "jeanteil",
    "summe",       # ok
]


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("csv_file")

    def handle(self, *args, **options):
        with open(options["csv_file"], newline="") as f:
            reader = csv.DictReader(f, fieldnames=COLS)
            for row in reader:
                if len(row["glv"]) == 3:
                    self.import_row(row)
                else:
                    self.stdout.write(self.style.WARNING("Invalid GL-Vnr: {}".format(row["glv"])))

    def import_row(self, row):
        try:
            subtype = self.get_subtype(row["glv"])
            subtype.shares = 1
            subtype.size = SubscriptionSize.objects.get(units=row["anteile"].replace(",", "."))
            subtype.price, *frac = row["summe"].split(",")
            if len(frac) > 0:
                frac, *_ = frac[0].split()
                if frac != "00":
                    self.stdout.write(self.style.WARNING("Cannot handle non-integer price: {}".format(row["summe"])))
            if subtype.price == "":
                subtype.price = 0
                self.stdout.write(self.style.WARNING("Invalid price: '{}'".format(row["summe"])))
            subtype.save()
        except SubscriptionSize.DoesNotExist:
            self.stdout.write(self.style.WARNING("Abogröße nicht vorhanden: {}".format(row["anteile"])))
        try:
            sub = self.get_sub(subtype, row)
            self.create_submember(sub, row)
            sub.nickname = row["nick"][:30]
            sub.save()
        except Depot.DoesNotExist:
            self.stdout.write(self.style.WARNING("Invalid VS-Nr: {}".format(row["vsnr"])))
        except (Share.DoesNotExist, ValueError, AttributeError):
            self.stdout.write(self.style.WARNING("Invalid GENO: {}".format(row["geno"])))
        except ValidationError:
            self.stdout.write(self.style.WARNING("Multiple use of GENO: {}".format(row["geno"])))

    def get_subtype(self, glv):
        subtype, _ = SubscriptionType.objects.get_or_create(
            name=glv, defaults={"required_assignments": 3, "price": 0, "size_id": 2})
        return subtype

    def get_sub(self, subtype, row):
        sub = Subscription.objects.filter(parts__type=subtype).first()
        if sub is None:
            depot = Depot.objects.get(pk=int(row["vsnr"]) + 1)
            sub = Subscription.objects.create(
                depot=depot,
                start_date=date.fromisoformat("2021-07-01"),
                activation_date=date())
            sub.parts.create(type=subtype)
        return sub

    def create_submember(self, sub, row):
        member = Share.objects.filter(number=row["geno"]).first().member
        SubscriptionMembership.objects.get_or_create(member=member, subscription=sub)
        sub.primary_member = member
