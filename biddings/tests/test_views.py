from django.test import TestCase
import pytest
from biddings.tests.mixins import (
    BiddingRoundMixin,
    MemberMixin,
    ViewPermissionsMixin,
)
from django.urls import reverse
from django.conf import settings


class BiddingRoundViewsTestCase(
    BiddingRoundMixin, MemberMixin, ViewPermissionsMixin, TestCase
):
    def setUp(self):
        self.primary_member = self.get_or_create_member(email="test@roko.li")

    # Required, otherweise these tests would fail in CI because the default value of SECRET_KEY is empty.
    @pytest.fixture(autouse=True)
    def override_secret_key(self):
        settings.SECRET_KEY = "test-secret-key"

    def test_secret_key(self):
        assert settings.SECRET_KEY == "test-secret-key"

    def test_list_login_required(self):
        url = reverse("biddingrounds")
        self.check_login_required(url)

    def test_list_view_template(self):
        self.client.force_login(self.primary_member.user)
        response = self.client.get(reverse("biddingrounds"))
        assert response.status_code == 200
        self.assertTemplateUsed(response, "biddings/biddinground_list.html")
