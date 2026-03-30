import os

from django.contrib.sites.models import Site
from django.core.management import BaseCommand
from django.template.loader import get_template
from juntagrico.entity.member import Member
from juntagrico.mailer import (
    EmailSender,
    organisation_subject,
)
from juntagrico.util.models import q_deactivated
from rotebeete.transitions.models import MemberTransition

test_email = os.getenv("ROTEBEETE_TEST_EMAIL") or "test@example.org"
print("test_email: ", test_email)


class Command(BaseCommand):
    def handle(self, *args, **options):
        members = Member.objects.filter(email=test_email)
        members = members.exclude(q_deactivated())
        print(f"Sending mails to {members.count()} members ...")
        for member in members:
            MemberTransition.objects.get_or_create(member=member)
            member.transition.data_needs_review = True
            member.transition.membership_needs_review = True
            member.transition.save()
        context = {
            "serverurl": "https://" + Site.objects.get_current().domain,
        }
        recipients = members.values_list("email", flat=True)
        for i in range(len(recipients) // 10 + 1):
            print(f"Sending chunk {i + 1} ...")
            EmailSender.get_sender(
                organisation_subject("Bitte Daten jetzt überprüfen"),
                get_template("mails/transition.txt").render(context),
                bcc=recipients[i * 10 : i * 10 + 10],
            ).send()
            print("Email Sent")
