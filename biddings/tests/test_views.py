from django.test import TestCase
from biddings.tests.mixins import (
    BiddingRoundMixin,
    MemberMixin,
    ViewPermissionsMixin,
)
from django.urls import reverse


class BiddingRoundViewsTestCase(
    BiddingRoundMixin, MemberMixin, ViewPermissionsMixin, TestCase
):
    def setUp(self):
        self.primary_member = self.get_or_create_member(email="test@roko.li")

    def test_list_login_required(self):
        url = reverse("biddingrounds")
        self.check_login_required(url)

    def test_list_view_template(self):
        self.client.force_login(self.primary_member.user)
        response = self.client.get(reverse("biddingrounds"))
        assert response.status_code == 200
        self.assertTemplateUsed(response, "biddings/biddinground_list.html")
