import datetime
import pytz
from freezegun import freeze_time

from django.test import TestCase
from django.test import override_settings

from .factories import (
    UserFactory,
    CustomerFactory,
    MassageFactory,
    UserProfileFactory,
)

tz = pytz.timezone("Europe/Ljubljana")


@override_settings(LANGUAGE_CODE="en-US")
class GeneralTest(TestCase):
    def test_check_auth_user_login(self):
        pass

    def test_check_un_auth_user_login(self):
        pass

    def test_custom_logout(self):
        therapist = UserFactory()
        self.client.force_login(therapist)
        response = self.client.get("/logout", follow=True)

        self.assertRedirects(response, "/accounts/login/?next=/")
        self.assertContains(response, text="Username")

    def test_homepage_loads(self):  # therapist already logged in
        therapist = UserFactory()
        self.client.force_login(therapist)
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="Appointments for")

    @freeze_time("2023-04-06 13:21:34", tz_offset=2)
    def test_check_listing_massage_views(self):
        therapist1 = UserProfileFactory(user__first_name="Jane").user
        therapist2 = UserProfileFactory().user
        self.client.force_login(therapist1)

        customer1 = CustomerFactory(name="Brian")
        customer2 = CustomerFactory(name="Alice")
        customer3 = CustomerFactory(name="David")
        customer4 = CustomerFactory(name="Jeanette")
        customer5 = CustomerFactory(name="Bob")
        customer6 = CustomerFactory(name="Cooper")

        MassageFactory(
            therapist=therapist1,
            customer=customer1,
            start=datetime.datetime(2023, 4, 6, 16, 0, 0).astimezone(tz=tz),
            status="approved",
        )
        MassageFactory(
            therapist=therapist1,
            customer=customer2,
            start=datetime.datetime(2023, 4, 6, 18, 0, 0).astimezone(tz=tz),
            status="canceled",
        )
        MassageFactory(
            therapist=therapist1,
            customer=customer3,
            start=datetime.datetime(2023, 4, 7, 17, 0, 0).astimezone(tz=tz),
        )
        MassageFactory(
            therapist=therapist1,
            customer=customer4,
            start=datetime.datetime(2023, 4, 5, 17, 0, 0).astimezone(tz=tz),
        )
        MassageFactory(
            therapist=therapist2,
            customer=customer5,
            start=datetime.datetime(2023, 4, 6, 19, 0, 0).astimezone(tz=tz),
        )
        MassageFactory(
            therapist=therapist2,
            customer=customer6,
            start=datetime.datetime(2023, 4, 4, 19, 0, 0).astimezone(tz=tz),
        )

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="Jane")
        # Brian should display
        self.assertContains(response, text="Brian")
        # Alice should not display because of status not "approved"
        self.assertNotContains(response, text="Alice")
        # David, Jeanette, Bob and Cooper should not display - wrong date/therapist
        self.assertNotContains(response, text="David")
        self.assertNotContains(response, text="Jeanette")
        self.assertNotContains(response, text="Bob")
        self.assertNotContains(response, text="Cooper")

    @freeze_time("2023-04-06 13:21:34", tz_offset=2)
    def test_main_concern_displays_on_index_page(self):
        therapist1 = UserProfileFactory(user__first_name="Jane").user
        self.client.force_login(therapist1)

        customer1 = CustomerFactory(name="Brian", main_concern="car accident")
        customer2 = CustomerFactory(name="Alice", main_concern="bike accident")
        customer3 = CustomerFactory(name="David", main_concern="fall off tree")

        MassageFactory(
            therapist=therapist1,
            customer=customer1,
            start=datetime.datetime(2023, 4, 6, 16, 0, 0).astimezone(tz=tz),
            status="approved",
        )
        MassageFactory(
            therapist=therapist1,
            customer=customer2,
            start=datetime.datetime(2023, 4, 6, 18, 0, 0).astimezone(tz=tz),
            status="canceled",
        )
        MassageFactory(
            therapist=therapist1,
            customer=customer3,
            start=datetime.datetime(2023, 4, 7, 17, 0, 0).astimezone(tz=tz),
            status="approved",
        )

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="Jane")
        self.assertContains(response, text="Appointments for")
        self.assertContains(response, text="Brian")
        self.assertNotContains(response, text="Alice")
        self.assertContains(response, text="car accident")
        # "bike accident" should not display because "Alice" status="canceled" and does not display
        self.assertNotContains(response, text="bike accident")
        # "fall off tree" should not display because "David" is not in today's massages and does not display
        self.assertNotContains(response, text="fall off tree")

    def test_check_access_permission(self):
        pass
