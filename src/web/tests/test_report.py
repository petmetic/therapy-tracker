from datetime import datetime
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

        cls.customer1 = CustomerFactory(name="Jane", surname="Doe")
        cls.customer2 = CustomerFactory(name="Adam")
        cls.customer3 = CustomerFactory(name="John")

        cls.service1 = ServiceFactory(payout=30, name="Massage 50 min", price=100)
        cls.service2 = ServiceFactory(payout=10, name="Massage 30 min", price=80)

        cls.massage1 = MassageFactory(
            therapist=cls.therapist1,
            customer=cls.customer1,
            service=cls.service1,
            start=datetime(2023, 8, 1, 17, 0, 0).astimezone(tz=tz),
        )
        cls.massage2 = MassageFactory(
            therapist=cls.therapist1,
            customer=cls.customer2,
            service=cls.service2,
            start=datetime(2023, 8, 1, 18, 0, 0).astimezone(tz=tz),
        )
        cls.massage3 = MassageFactory(
            therapist=cls.therapist1,
            customer=cls.customer3,
            service=cls.service1,
            start=datetime(2023, 8, 10, 17, 0, 0).astimezone(tz=tz),
        )
        cls.massage4 = MassageFactory(
            therapist=cls.therapist1,
            customer=cls.customer1,
            service=cls.service1,
            start=datetime(2023, 7, 1, 17, 0, 0).astimezone(tz=tz),
        )

    def test_reports_page_displays(self):
        self.client.force_login(self.therapist1)

        response = self.client.get(reverse("reports"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="Breakdown of Hours")

    def test_report_date_displays_in_url(self):
        self.client.force_login(self.therapist1)

        start_date = "2023-08-01"
        end_date = "2023-08-31"

        response = self.client.get(
            f"{reverse('reports')}?start-date={start_date}1&end-date={end_date}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"start-date={start_date}")
        self.assertContains(response, f"end-date={end_date}")

    def test_report_hours_page_loads(self):
        self.client.force_login(self.therapist1)

        start_date = "2023-08-01"
        end_date = "2023-08-31"

        response = self.client.get(
            f"{reverse('report_hours')}?start-date={start_date}&end-date={end_date}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"start-date={start_date}")
        self.assertContains(response, f"end-date={end_date}")

        # All therapists should display
        self.assertContains(response, text="Alice")
        self.assertContains(response, text="Charlotte")
        self.assertContains(response, text="Mike")

        # display date should be: "date: 1. Aug 2023 - 31. Aug 2023"
        self.assertContains(response, text="1. Aug 2023 - 31. Aug 2023")

    def test_report_hours_detail_page_displays_w_correct_date(self):
        # http://127.0.0.1:8000/report_hours_detail/2/?start-date=2023-09-01&end-date=2023-09-30
        #  4. Sep 2023 ob 14:00	Masten, Igor	Masaža 50 minut	0 eur	25 eur

        self.client.force_login(self.therapist1)

        start_date = "2023-08-01"
        end_date = "2023-08-31"

        response = self.client.get(
            f"{reverse('report_hours_detail', kwargs={'pk': self.therapist2.pk})}?start-date={start_date}&end-date={end_date}"
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, text="Charlotte")
        self.assertContains(response, text="30")
        self.assertNotContains(response, text="Logout: Charlotte")
        self.assertContains(response, text="Logout: Alice")
        self.assertContains(response, text="Therapist:")
        self.assertNotContains(response, text="Mike")

        # date out of range of search (month of August)
        self.assertNotContains(response, text="1. Jul 2023 at 17:00")

        self.assertContains(response, text="1. Aug 2023 at 17:00")
        self.assertContains(response, text="Jane")
        self.assertContains(response, text="100")
        self.assertContains(response, text="30")

        self.assertContains(response, text="1. Aug 2023 at 18:00")
        self.assertContains(response, text="Adam")
        self.assertContains(response, text="80")
        self.assertContains(response, text="10")

        self.assertContains(response, text="Massage 50 min")
