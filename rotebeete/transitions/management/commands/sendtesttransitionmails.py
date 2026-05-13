import os
from juntagrico.entity.member import Member
from juntagrico.util.models import q_deactivated

from .sendtransitionmails import Command as TransitionCommand

# Send a test email and activate member transition
# Set env ROTEBEETE_TEST_EMAIL or provide an email
# example: uv run python manage.py sendtesttransitionmails rotebeete@rotebeete.org

default_test_email = os.getenv("ROTEBEETE_TEST_EMAIL") or "test@example.org"


class Command(TransitionCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "email",
            nargs="?",
            help="Override the configured test email address for this run.",
        )

    def get_members(self, options):
        recipient_email = options["email"] or default_test_email
        members = Member.objects.filter(email=recipient_email).exclude(q_deactivated())
        self.stdout.write(f"test_email: {recipient_email}")
        return members
