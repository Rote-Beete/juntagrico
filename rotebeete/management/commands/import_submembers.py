import csv
import sys
from datetime import date

from django.core.exceptions import ValidationError, ObjectDoesNotExist, MultipleObjectsReturned
from django.core.management.base import BaseCommand
from juntagrico.entity.depot import Depot
from juntagrico.entity.subtypes import SubscriptionSize, SubscriptionType
from juntagrico.models import Member, Share, Subscription, SubscriptionMembership


COLS = [
    "glv",
    "vorname",
    "name",
    "vsnr",
    "verteiler",
    "mail",
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
        glv = row["glv"]
        member, _ = Member.objects.get_or_create(
            email=row["mail"], defaults={"first_name": row["vorname"], "last_name": row["name"]})
        try:
            subtype = SubscriptionType.objects.get(name=glv)
            sub = Subscription.objects.get(parts__type=subtype)
            SubscriptionMembership.objects.get_or_create(member=member, subscription=sub)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            self.stdout.write(self.style.WARNING("Abo/Typ not yet existing: {} (member {})".format(glv, member)))
        except ValidationError:
            self.stdout.write(self.style.WARNING("Member already has another Abo: {}".format(member)))
