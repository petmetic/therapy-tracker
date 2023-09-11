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
        """
        The superuser(Alice) wants to see the massages of "Charlotte" from 1.Aug - 31. Aug 2023.
        The massages that must be seen are: massage1, massage2.
        Massage3  is from therapist Mike and should not be shown.

        """
        cls.therapist1 = UserFactory(
            is_superuser=True, is_staff=True, first_name="Alice"
        )
        cls.therapist2 = UserFactory(first_name="Charlotte")
        cls.therapist3 = UserFactory(first_name="Mike")

        cls.customer1 = CustomerFactory(name="Jane", surname="Doe")
        cls.customer2 = CustomerFactory(name="Adam")
        cls.customer3 = CustomerFactory(name="John")

        cls.service1 = ServiceFactory(payout="15", name="Massage 50 min", price="45")
        cls.service2 = ServiceFactory(payout="5", name="Massage 30 min", price="80")

        cls.massage1 = MassageFactory(
            therapist=cls.therapist2,
            customer=cls.customer1,
            service=cls.service1,
            start=datetime(2023, 8, 1, 17, 0, 0).astimezone(tz=tz),
        )
        cls.massage2 = MassageFactory(
            therapist=cls.therapist2,
            customer=cls.customer2,
            service=cls.service2,
            start=datetime(2023, 8, 1, 18, 0, 0).astimezone(tz=tz),
        )
        cls.massage3 = MassageFactory(
            therapist=cls.therapist3,
            customer=cls.customer3,
            service=cls.service1,
            start=datetime(2023, 8, 10, 17, 0, 0).astimezone(tz=tz),
        )
        cls.massage4 = MassageFactory(
            therapist=cls.therapist2,
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
        self.client.force_login(self.therapist1)

        start_date = "2023-08-01"
        end_date = "2023-08-31"

        response = self.client.get(
            f"{reverse('report_hours_detail', kwargs={'pk': self.therapist2.pk})}?start-date={start_date}&end-date={end_date}"
        )

        self.assertEqual(response.status_code, 200)

        # assert right superuser (Alice) is logged in and can see "Charlotte"
        self.assertNotContains(response, text="Logout: Charlotte")
        self.assertContains(response, text="Logout: Alice")

        # date  in range of search (month of August)
        self.assertContains(response, text="1. Aug 2023 - 31. Aug 2023")
        # date out of range of search (month of August)
        self.assertNotContains(response, text="1. Jul 2023 at 17:00")

        # assert right therapist (Charlotte) is shown
        self.assertContains(response, text="Therapist:")
        self.assertNotContains(response, text="Mike")
        self.assertContains(response, text="Charlotte")

        # Massage 50 min of 1.8.2023 at 17.00, customer='Doe, Jane', amount paid="45", Amount Due to therapist="15"
        self.assertContains(response, text="1. Aug 2023 at 17:00")
        self.assertContains(response, text="Doe, Jane")
        self.assertContains(response, text="Massage 50 min")
        self.assertContains(response, text="Amount Paid")
        self.assertContains(response, text="45")
        self.assertContains(response, text="Amount Due to Therapist")
        self.assertContains(response, text="15")

        # Massage 30 min of 1.8.2023 at 18.00, customer='Adam', amount paid="80, Amount Due to therapist="5"
        self.assertContains(response, text="Adam")
        self.assertContains(response, text="80")
        self.assertContains(response, text="Amount Paid")
        self.assertContains(response, text="5")
        self.assertContains(response, text="Massage 30 min")

        self.assertNotContains(response, text="John")
