import csv
import sys
from datetime import date

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from juntagrico.entity.depot import Depot
from juntagrico.entity.subtypes import SubscriptionSize, SubscriptionType
from juntagrico.models import Share, Subscription, SubscriptionMembership


COLS = [
    "glv",
    "size",
    "perpart",
    "price",
]


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("csv_file")

    def handle(self, *args, **options):
        with open(options["csv_file"], newline="") as f:
            reader = csv.DictReader(f, fieldnames=COLS, dialect="excel-tab")
            for row in reader:
                if len(row["glv"]) == 3:
                    self.import_row(row)
                else:
                    self.stdout.write(self.style.WARNING("Invalid GL-Vnr: {}".format(row["glv"])))

    def import_row(self, row):
        try:
            subtype = self.get_subtype(row["glv"])
            subtype.size = SubscriptionSize.objects.get(units=row["size"].replace(",", "."))
            subtype.price = row["price"].replace(",", ".")
            # print(subtype.name, subtype.size, subtype.price)
            subtype.save()
        except SubscriptionType.DoesNotExist:
            self.stdout.write(self.style.WARNING("Gemüseanteil-Typ nicht vorhanden: {}".format(row["glv"])))
        except SubscriptionType.MultipleObjectsReturned:
            self.stdout.write(self.style.WARNING("Gemüseanteil-Typ doppelt: {}".format(row["glv"])))

    def get_subtype(self, glv):
        return SubscriptionType.objects.get(name=glv)
