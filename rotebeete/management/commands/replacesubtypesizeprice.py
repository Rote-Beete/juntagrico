import csv

from django.core.management.base import BaseCommand
from juntagrico.entity.subtypes import SubscriptionSize, SubscriptionType


COLS = [
    "glv",
    "size",
    "price",
]


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("csv_file")

    def handle(self, *args, **options):
        with open(options["csv_file"], newline="") as f:
            # reader = csv.DictReader(f, fieldnames=COLS, dialect="excel-tab")
            reader = csv.DictReader(f, fieldnames=COLS, delimiter=",")
            for row in reader:
                if len(row["glv"]) == 3:
                    self.import_row(row)
                else:
                    self.stdout.write(
                        self.style.WARNING("Invalid GL-Vnr: {}".format(row["glv"]))
                    )

    def import_row(self, row):
        try:
            # print(f"glv: {row['glv']}, size: {row['size']}, price: {row['price']}")
            subtype = self.get_subtype(row["glv"])
            print(f"name: {subtype.name}, size: {subtype.size}, price: {subtype.price}")
            subtype.size = SubscriptionSize.objects.get(
                units=row["size"].replace(",", ".")
            )
            subtype.price = row["price"].replace(",", ".")
            print(f"name: {subtype.name}, size: {subtype.size}, price: {subtype.price}")
            # subtype.save()
        except SubscriptionType.DoesNotExist:
            self.stdout.write(
                self.style.WARNING(f"Gemüseanteil-Typ nicht vorhanden: {row['glv']}")
            )
        except SubscriptionType.MultipleObjectsReturned:
            self.stdout.write(
                self.style.WARNING("Gemüseanteil-Typ doppelt: {}".format(row["glv"]))
            )

    def get_subtype(self, glv):
        return SubscriptionType.objects.get(name=glv)
