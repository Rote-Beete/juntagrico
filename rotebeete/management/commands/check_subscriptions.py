import csv
import sys
from datetime import date

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from juntagrico.entity.depot import Depot
from juntagrico.entity.subtypes import SubscriptionSize, SubscriptionType
from juntagrico.models import Share, Subscription, SubscriptionMembership


class Command(BaseCommand):
    def handle(self, *args, **options):
        for sub in Subscription.objects.all():
            if sub.primary_member is None:
                self.stdout.write(self.style.ERROR("Subscription {} has no primary member.".format(sub.id)))
