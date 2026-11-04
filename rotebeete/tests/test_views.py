import csv
import io
from datetime import date

from django.contrib.auth.models import User
from django.test import override_settings, RequestFactory
from juntagrico.entity.depot import Depot
from juntagrico.entity.location import Location
from juntagrico.entity.subs import Subscription
from juntagrico.entity.subtypes import (
    ProductSize,
    SubscriptionBundle,
    SubscriptionProduct,
    SubscriptionType,
)
from juntagrico.tests import JuntagricoTestCase

from rotebeete.exports.views import (
    export_depot_emails,
    export_depot_list,
    export_depot_overview,
    export_members,
    export_subscriptions,
    _subtype_units,
    get_status,
)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class ExportTestCase(JuntagricoTestCase):
    """Base class for export tests that loads only member/area fixtures.

    JuntagricoTestCase.setUpTestData creates depots and subscriptions that
    would pollute the export tests, so we override it to load only the
    member and area fixtures needed for create_member/create_paid_share.
    """

    @classmethod
    def setUpTestData(cls):
        cls.load_members()
        cls.default_member = cls.member
        cls.load_areas()


def _parse_members_csv(content):
    """Parse the members CSV which has 4 header rows before data."""
    lines = io.StringIO(content).readlines()
    # Row 0: title, Row 1: empty, Row 2: section headers, Row 3: column names
    # Row 4+: data rows
    # The column names are in row 3, but the first column header is empty (GenoNr. is in row 2)
    # We build fieldnames from rows 2 and 3 combined
    header2 = next(csv.reader([lines[2]]))
    header3 = next(csv.reader([lines[3]]))
    # Combine: use header2 where header3 is empty
    fieldnames = []
    for h2, h3 in zip(header2, header3):
        fieldnames.append(h3 if h3 else h2)
    data_lines = lines[4:]
    reader = csv.DictReader(io.StringIO("".join(data_lines)), fieldnames=fieldnames)
    return list(reader)


def read_csv_rows(response):
    """Helper to parse CSV response content into a list of dicts."""
    reader = csv.DictReader(io.StringIO(response.content.decode("utf-8")))
    return list(reader)


def make_request():
    factory = RequestFactory()
    request = factory.get("/export")
    request.user = User.objects.create_user(username="admin", password="pass")
    return request


def create_depot(name, weekday=1):
    location = Location.objects.create(
        name=f"Location for {name}", latitude="47.0", longitude="11.0",
        addr_street="Depotstr. 1", addr_zipcode="1234",
        addr_location="Teststadt",
    )
    return Depot.objects.create(name=name, weekday=weekday, location=location)


def create_subscription_type(name="Ganze", price=100, required_assignments=4):
    product = SubscriptionProduct.objects.create(name="Gemüse")
    size = ProductSize.objects.create(name=name, units=1.0, product=product)
    bundle = SubscriptionBundle.objects.create(long_name=name)
    bundle.product_sizes.add(size)
    return SubscriptionType.objects.create(
        name=name, price=price, required_assignments=required_assignments, bundle=bundle,
    )


def create_subscription(depot, primary_member, start_date=None, activation_date=None,
                        deactivation_date=None, nickname=None, end_date=None,
                        cancellation_date=None):
    if start_date is None:
        start_date = date(2024, 1, 1)
    if activation_date is None:
        activation_date = start_date
    if nickname is None:
        nickname = f"Sub of {primary_member.first_name}"
    # If deactivation_date is set, end_date and cancellation_date must also be set
    if deactivation_date and end_date is None:
        end_date = deactivation_date
    if deactivation_date and cancellation_date is None:
        cancellation_date = deactivation_date
    sub = Subscription.objects.create(
        depot=depot, start_date=start_date, activation_date=activation_date,
        cancellation_date=cancellation_date, deactivation_date=deactivation_date,
        nickname=nickname, end_date=end_date, notes="",
    )
    # Primary member must be a membership first (validation requirement)
    sub.subscriptionmembership_set.create(member=primary_member, join_date=start_date)
    sub.primary_member = primary_member
    sub.save()
    return sub


class TestGetStatus(ExportTestCase):
    def test_active_subscription(self):
        sub = Subscription(start_date=date(2024, 1, 1), activation_date=date(2024, 1, 1))
        self.assertEqual(get_status(sub), "aktiv")

    def test_ended_subscription(self):
        sub = Subscription(start_date=date(2024, 1, 1), activation_date=date(2024, 1, 1),
                           deactivation_date=date(2024, 1, 1))
        self.assertEqual(get_status(sub), "beendet")

    def test_waiting_subscription(self):
        sub = Subscription(start_date=date(2099, 1, 1))
        self.assertEqual(get_status(sub), "wartend")

    def test_undefined_status(self):
        # A bare Subscription has default start_date in the future, so it's "wartend"
        # To get "undefiniert", all date fields must be None
        sub = Subscription()
        sub.start_date = None
        self.assertEqual(get_status(sub), "undefiniert")

    def test_terminated_subscription(self):
        # end_date set and >= today means "gekündigt"
        sub = Subscription(start_date=date(2024, 1, 1), activation_date=date(2024, 1, 1),
                           end_date=date(2099, 1, 1))
        self.assertEqual(get_status(sub), "gekündigt")


class TestSubtypeUnits(ExportTestCase):
    def test_single_product_size(self):
        st = create_subscription_type(name="Ganze", price=100)
        self.assertEqual(_subtype_units(st), 1.0)

    def test_half_size(self):
        product = SubscriptionProduct.objects.create(name="Gemüse")
        size = ProductSize.objects.create(name="Halbe", units=0.5, product=product)
        bundle = SubscriptionBundle.objects.create(long_name="Halbe")
        bundle.product_sizes.add(size)
        st = SubscriptionType.objects.create(name="Halbe", price=50, required_assignments=2, bundle=bundle)
        self.assertEqual(_subtype_units(st), 0.5)


class TestExportDepotList(ExportTestCase):
    def test_empty(self):
        response = export_depot_list(make_request())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        rows = read_csv_rows(response)
        self.assertEqual(len(rows), 0)

    def test_single_active_subscription(self):
        depot = create_depot(name="Depot A")
        member = ExportTestCase.create_member(email="test1@test.li")
        st = create_subscription_type(name="Ganze", price=100)
        sub = create_subscription(depot, member)
        sub.parts.create(type=st)

        response = export_depot_list(make_request())
        rows = read_csv_rows(response)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["Verteilstation"], "Depot A")
        self.assertEqual(rows[0]["GLV-Nr."], "Ganze")
        self.assertEqual(rows[0]["Anteil/e"], "1.0")

    def test_multiple_depots(self):
        depot_a = create_depot(name="Depot A")
        depot_b = create_depot(name="Depot B")
        member_a = ExportTestCase.create_member(email="a@test.li")
        member_b = ExportTestCase.create_member(email="b@test.li")
        st = create_subscription_type(name="Ganze", price=100)

        sub_a = create_subscription(depot_a, member_a)
        sub_a.parts.create(type=st)
        sub_b = create_subscription(depot_b, member_b)
        sub_b.parts.create(type=st)

        response = export_depot_list(make_request())
        rows = read_csv_rows(response)
        self.assertEqual(len(rows), 2)
        depot_names = [r["Verteilstation"] for r in rows]
        self.assertIn("Depot A", depot_names)
        self.assertIn("Depot B", depot_names)

    def test_inactive_subscription_excluded(self):
        depot = create_depot(name="Depot A")
        member = ExportTestCase.create_member(email="test2@test.li")
        st = create_subscription_type(name="Ganze", price=100)
        # Create active subscription first, add part, then deactivate
        sub = create_subscription(
            depot, member,
            activation_date=date(2024, 1, 1),
        )
        sub.parts.create(type=st)
        # Now deactivate the subscription
        sub.cancellation_date = date(2024, 6, 1)
        sub.deactivation_date = date(2024, 6, 1)
        sub.end_date = date(2024, 6, 1)
        sub.save()

        response = export_depot_list(make_request())
        rows = read_csv_rows(response)
        self.assertEqual(len(rows), 0)

    def test_nickname_used_when_present(self):
        depot = create_depot(name="Depot A")
        member = ExportTestCase.create_member(email="test3@test.li")
        st = create_subscription_type(name="Ganze", price=100)
        sub = create_subscription(depot, member, nickname="Familie Müller")
        sub.parts.create(type=st)

        response = export_depot_list(make_request())
        rows = read_csv_rows(response)
        self.assertEqual(rows[0]["Gruppenbezeichnung / Name"], "Familie Müller")


class TestExportDepotOverview(ExportTestCase):
    def test_empty(self):
        response = export_depot_overview(make_request())
        self.assertEqual(response.status_code, 200)
        rows = read_csv_rows(response)
        self.assertEqual(len(rows), 0)

    def test_single_depot_with_subscriptions(self):
        depot = create_depot(name="Depot A")
        member = ExportTestCase.create_member(email="test4@test.li")
        st = create_subscription_type(name="Ganze", price=100)
        sub = create_subscription(depot, member)
        sub.parts.create(type=st)

        response = export_depot_overview(make_request())
        rows = read_csv_rows(response)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["Verteilstation"], "Depot A")
        self.assertEqual(rows[0]["Anteile"], "1")

    def test_multiple_parts_summed(self):
        depot = create_depot(name="Depot A")
        member = ExportTestCase.create_member(email="test5@test.li")
        st = create_subscription_type(name="Ganze", price=100)
        sub = create_subscription(depot, member)
        sub.parts.create(type=st)
        sub.parts.create(type=st)

        response = export_depot_overview(make_request())
        rows = read_csv_rows(response)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["Anteile"], "2")

    def test_inactive_excluded(self):
        depot = create_depot(name="Depot A")
        member = ExportTestCase.create_member(email="test6@test.li")
        st = create_subscription_type(name="Ganze", price=100)
        # Create active subscription first, add part, then deactivate
        sub = create_subscription(
            depot, member,
            activation_date=date(2024, 1, 1),
        )
        sub.parts.create(type=st)
        # Now deactivate the subscription
        sub.cancellation_date = date(2024, 6, 1)
        sub.deactivation_date = date(2024, 6, 1)
        sub.end_date = date(2024, 6, 1)
        sub.save()

        response = export_depot_overview(make_request())
        rows = read_csv_rows(response)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["Verteilstation"], "Depot A")
        self.assertEqual(rows[0]["Anteile"], "0")

    def test_multiple_depots_ordered(self):
        depot_b = create_depot(name="Depot B")
        depot_a = create_depot(name="Depot A")
        member = ExportTestCase.create_member(email="test7@test.li")
        st = create_subscription_type(name="Ganze", price=100)
        sub_a = create_subscription(depot_a, member)
        sub_a.parts.create(type=st)
        member2 = ExportTestCase.create_member(email="m2@test.li")
        sub_b = create_subscription(depot_b, member2)
        sub_b.parts.create(type=st)

        response = export_depot_overview(make_request())
        rows = read_csv_rows(response)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["Verteilstation"], "Depot A")
        self.assertEqual(rows[1]["Verteilstation"], "Depot B")


class TestExportDepotEmails(ExportTestCase):
    def test_empty(self):
        response = export_depot_emails(make_request())
        rows = read_csv_rows(response)
        self.assertEqual(len(rows), 0)

    def test_emails_per_depot(self):
        depot = create_depot(name="Depot A")
        member = ExportTestCase.create_member(email="member@test.li")
        st = create_subscription_type(name="Ganze", price=100)
        sub = create_subscription(depot, member)
        sub.parts.create(type=st)

        response = export_depot_emails(make_request())
        rows = read_csv_rows(response)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["Verteilstation"], "Depot A")
        self.assertEqual(rows[0]["E-Mail-Adresse"], "member@test.li")

    def test_multiple_memberships(self):
        depot = create_depot(name="Depot A")
        member1 = ExportTestCase.create_member(email="m1@test.li")
        member2 = ExportTestCase.create_member(email="m2@test.li")
        st = create_subscription_type(name="Ganze", price=100)
        sub = create_subscription(depot, member1)
        sub.subscriptionmembership_set.create(member=member2)
        sub.parts.create(type=st)

        response = export_depot_emails(make_request())
        rows = read_csv_rows(response)
        emails = [r["E-Mail-Adresse"] for r in rows]
        self.assertIn("m1@test.li", emails)
        self.assertIn("m2@test.li", emails)

    def test_left_membership_excluded(self):
        depot = create_depot(name="Depot A")
        member1 = ExportTestCase.create_member(email="m1@test.li")
        member2 = ExportTestCase.create_member(email="m2@test.li")
        st = create_subscription_type(name="Ganze", price=100)
        sub = create_subscription(depot, member1)
        sub.subscriptionmembership_set.create(member=member2, join_date=date(2024, 1, 1), leave_date=date(2024, 1, 1))
        sub.parts.create(type=st)

        response = export_depot_emails(make_request())
        rows = read_csv_rows(response)
        emails = [r["E-Mail-Adresse"] for r in rows]
        self.assertIn("m1@test.li", emails)
        self.assertNotIn("m2@test.li", emails)


class TestExportSubscriptions(ExportTestCase):
    def test_empty(self):
        response = export_subscriptions(make_request())
        self.assertEqual(response.status_code, 200)
        rows = read_csv_rows(response)
        # Summary row with totals
        self.assertGreaterEqual(len(rows), 1)

    def test_subscription_export_fields(self):
        depot = create_depot(name="Depot A")
        member = ExportTestCase.create_member(email="member@test.li", phone="0123456")
        st = create_subscription_type(name="Ganze", price=100)
        sub = create_subscription(depot, member)
        sub.parts.create(type=st)

        response = export_subscriptions(make_request())
        rows = read_csv_rows(response)
        # Find the data row (not the summary row)
        data_rows = [r for r in rows if r.get("HauptbezieherIn")]
        self.assertEqual(len(data_rows), 1)
        row = data_rows[0]
        self.assertEqual(row["GLV-Nr."], "Ganze")
        self.assertEqual(row["HauptbezieherIn"], "last_name, first_name")
        self.assertEqual(row["HauptbezieherInEmail"], "member@test.li")
        self.assertEqual(row["Verteilstation"], "Depot A")
        self.assertEqual(row["Status"], "aktiv")

    def test_summary_row_totals(self):
        depot = create_depot(name="Depot A")
        member = ExportTestCase.create_member(email="test8@test.li")
        st = create_subscription_type(name="Ganze", price=100)
        sub = create_subscription(depot, member)
        sub.parts.create(type=st)

        response = export_subscriptions(make_request())
        rows = read_csv_rows(response)
        # Last row is the summary
        summary = rows[-1]
        self.assertEqual(summary["Preis"], "100.00")


class TestExportMembers(ExportTestCase):
    def test_empty(self):
        response = export_members(make_request())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")

    def test_member_without_share_excluded(self):
        # Members without shares are not included in the export
        ExportTestCase.create_member(email="member@test.li")

        response = export_members(make_request())
        content = response.content.decode("utf-8")
        rows = _parse_members_csv(content)
        # No data rows — member without share is excluded
        self.assertEqual(len(rows), 0)

