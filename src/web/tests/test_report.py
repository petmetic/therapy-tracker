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
@freeze_time("2023-9-1 13:21:34", tz_offset=2)
class ReportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.therapist1 = UserFactory(
            is_superuser=True, is_staff=True, first_name="Alice"
        )
        cls.therapist2 = UserFactory(first_name="Charlotte")
        cls.therapist3 = UserFactory(first_name="Mike")

        cls.customer1 = CustomerFactory(name="Jane")
        cls.customer2 = CustomerFactory(name="Adam")
        cls.customer3 = CustomerFactory(name="John")
        cls.massage1 = MassageFactory(
            therapist=cls.therapist1,
            customer=cls.customer1,
            start=datetime.datetime(2023, 8, 1, 17, 0, 0).astimezone(tz=tz),
        )
        cls.massage2 = MassageFactory(
            therapist=cls.therapist1,
            customer=cls.customer2,
            start=datetime.datetime(2023, 8, 1, 18, 0, 0).astimezone(tz=tz),
        )
        cls.massage3 = MassageFactory(
            therapist=cls.therapist1,
            customer=cls.customer3,
            start=datetime.datetime(2023, 8, 10, 17, 0, 0).astimezone(tz=tz),
        )
        cls.massage4 = MassageFactory(
            therapist=cls.therapist1,
            customer=cls.customer1,
            start=datetime.datetime(2023, 7, 1, 17, 0, 0).astimezone(tz=tz),
        )
        cls.massage5 = MassageFactory()
        cls.massage6 = MassageFactory()

        cls.service1 = ServiceFactory(payout=30)

    def test_reports_page_displays(self):
        self.client.force_login(self.therapist1)

        response = self.client.get(reverse("reports"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="Breakdown of Hours")

    def test_report_date_displays_in_url(self):
        self.client.force_login(self.therapist1)

        response = self.client.get(reverse("reports"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="Breakdown of Hours")

        start_date = "2023-08-01"
        end_date = "2023-08-31"

        response = self.client.get(
            "/report_hours/?start-date=2023-08-01&end-date=2023-08-31"
        )
        self.assertContains(response, "value={start_date}")
        self.assertContains(response, "value={end_date}")

    def test_report_hours_page_loads(self):
        self.client.force_login(self.therapist1)

        start_date = "2023-08-01"
        end_date = "2023-08-31"

        response = self.client.get(reverse("report_hours"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="Breakdown of Hours")

        # All therapists should display
        self.assertContains(response, text="Alice")
        self.assertContains(response, text="Charlotte")
        self.assertContains(response, text="Mike")

        # display date should be: "date: 1. Aug 2023 - 31. Aug 2023"
        self.assertContains(response, text="date: 1. Aug 2023 - 31. Aug 2023")

    def test_report_hours_detail_page_displays_w_correct_date(self):
        self.client.force_login(self.therapist1)

        start_date = "2023-08-01"
        end_date = "2023-08-31"

        response = self.client.get(
            reverse("report_hours_detail"),
            kwargs={
                "pk": self.therapist.pk,
                "start-date": start_date,
                "end-date": end_date,
            },
        )
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, text="Alice")
        self.assertContains(response, text="Therapist:")
