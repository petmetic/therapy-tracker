import datetime
import pytz

from django.test import TestCase
from django.urls import reverse
from django.test import override_settings
from freezegun import freeze_time

from .factories import (
    UserFactory,
    CustomerFactory,
    MassageFactory,
    ServiceFactory,
)

tz = pytz.timezone("Europe/Ljubljana")


@override_settings(LANGUAGE_CODE="en-US")
@freeze_time("2023-8-1 13:21:34", tz_offset=2)
class ReportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.therapist1 = UserFactory(is_superuser=True, is_staff=True)
        cls.therapist2 = UserFactory()
        cls.customer1 = CustomerFactory(name="Jane")
        cls.customer2 = CustomerFactory(name="Adam")
        cls.customer3 = CustomerFactory(name="John")
        cls.massage1 = MassageFactory(
            therapist=cls.therapist1,
            customer=cls.customer1,
            start=datetime.datetime(2023, 8, 1, 17, 0, 0).astimezone(tz=tz),
        )
        cls.massage2 = MassageFactory()
        cls.massage3 = MassageFactory()
        cls.massage4 = MassageFactory()
        cls.massage5 = MassageFactory()
        cls.massage6 = MassageFactory()

        cls.service1 = ServiceFactory(payout=30)

    def test_reports_page_displays(self):
        self.client.force_login(self.therapist1)

        response = self.client.get(reverse("reports"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="Breakdown of Hours")

    def test_report_date_displays(self):
        pass
