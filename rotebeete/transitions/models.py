from django.db import models


class MemberTransition(models.Model):
    member = models.OneToOneField(
        "juntagrico.Member", on_delete=models.CASCADE, related_name="transition"
    )
    data_needs_review = models.BooleanField(default=False)
    membership_needs_review = models.BooleanField(default=False)

    def __str__(self):
        return str(self.member)
