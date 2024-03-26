from django.contrib.sites.models import Site
from django.core.management import BaseCommand
from django.template.loader import get_template
from juntagrico.config import Config
from juntagrico.dao.memberdao import MemberDao
from juntagrico.entity.member import Member
from juntagrico.mailer import formemails
from juntagrico.util.models import q_deactivated


class Command(BaseCommand):
    def handle(self, *args, **options):
        # members = Member.objects.get(email="test@example.org")
        members = Member.objects.filter(MemberDao.has_subscription())
        members = members.exclude(q_deactivated())
        print(f"Sending mails to {members.count()} members ...")
        for member in members:
            member.transition.data_needs_review = True
            member.transition.membership_needs_review = True
            member.transition.save()
        context = {
            "serverurl": "https://" + Site.objects.get_current().domain,
        }
        formemails.internal(
            "Überprüfe deine Daten",
            get_template("mails/transition.html").render(context),
            get_template("mails/transition.txt").render(context),
            members.values_list("email", flat=True),
            [],
            Config.info_email(),
        )
