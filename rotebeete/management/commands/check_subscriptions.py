from django.core.management.base import BaseCommand
from juntagrico.models import Subscription


class Command(BaseCommand):
    def handle(self, *args, **options):
        for sub in Subscription.objects.all():
            if sub.primary_member is None:
                self.stdout.write(
                    self.style.ERROR(
                        "Subscription {} has no primary member.".format(sub.id)
                    )
                )
