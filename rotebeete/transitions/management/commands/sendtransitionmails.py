from django.contrib.sites.models import Site
from django.core.management import BaseCommand
from django.template.loader import get_template
from juntagrico.entity.member import Member
from juntagrico.mailer import (
    EmailSender,
    organisation_subject,
)
from juntagrico.util.models import q_deactivated


class Command(BaseCommand):
    def handle(self, *args, **options):
        members = Member.objects.filter(email="test@example.org")
        # members = Member.objects.filter(MemberDao.has_subscription())
        members = members.exclude(q_deactivated())
        print(f"Sending mails to {members.count()} members ...")
        for member in members:
            member.transition.data_needs_review = True
            member.transition.membership_needs_review = True
            member.transition.save()
        context = {
            "serverurl": "https://" + Site.objects.get_current().domain,
        }
        EmailSender.get_sender(
            organisation_subject("Bitte Daten jetzt überprüfen"),
            get_template("mails/transition.txt").render(context),
            bcc=members.values_list("email", flat=True),
        ).send()
