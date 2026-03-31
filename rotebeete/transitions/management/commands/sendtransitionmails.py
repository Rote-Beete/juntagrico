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


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--yes",
            action="store_true",
            help="Send emails without interactive confirmation.",
        )

    def handle(self, *args, **options):
        from juntagrico.dao.memberdao import MemberDao

        members = Member.objects.filter(MemberDao.has_subscription())
        members = members.exclude(q_deactivated())
        recipient_count = members.count()

        if recipient_count == 0:
            self.stdout.write("No active members found. No emails will be sent.")
            return

        self.stdout.write(f"{recipient_count} email(s) will be sent.")
        self.stdout.write(f"EMAIL_HOST: {os.getenv('ROTEBEETE_EMAIL_HOST')}")
        self.stdout.write(f"EMAIL_HOST_USER: {os.getenv('ROTEBEETE_EMAIL_HOST_USER')}")
        self.stdout.write(
            f"EMAIL_HOST_PASSWORD: {os.getenv('ROTEBEETE_EMAIL_HOST_PASSWORD')}"
        )
        self.stdout.write(f"EMAIL_PORT: {os.getenv('ROTEBEETE_EMAIL_PORT')}")
        self.stdout.write(f"EMAIL_USE_SSL: {os.getenv('ROTEBEETE_EMAIL_USE_SSL')}")
        self.stdout.write(f"EMAIL_USE_TLS: {os.getenv('ROTEBEETE_EMAIL_USE_TLS')}")
        self.stdout.write(
            f"DEFAULT_FROM_EMAIL: {os.getenv('ROTEBEETE_DEFAULT_FROM_EMAIL')}"
        )
        self.stdout.write(
            f"EMAIL_WHITELIST_EMAILS: {os.getenv('ROTEBEETE_WHITELIST_EMAILS')}"
        )

        if not options["yes"]:
            confirmation = input("Agreed? (yes/no): ").strip().lower()
            if confirmation not in {"y", "yes"}:
                self.stdout.write("Aborted. No emails were sent.")
                return

        self.stdout.write(f"Sending mails to {recipient_count} members ...")
        for member in members:
            transition, _ = MemberTransition.objects.get_or_create(member=member)
            transition.data_needs_review = True
            transition.membership_needs_review = True
            transition.save()
        context = {
            "serverurl": "https://" + Site.objects.get_current().domain,
        }
        recipients = list(members.values_list("email", flat=True))
        for chunk_index, start in enumerate(range(0, len(recipients), 10), start=1):
            self.stdout.write(f"Sending chunk {chunk_index} ...")
            EmailSender.get_sender(
                organisation_subject("Bitte Daten jetzt überprüfen"),
                get_template("mails/transition.txt").render(context),
                bcc=recipients[start : start + 10],
            ).send()
            self.stdout.write("Email sent")
