import pytz

from django.test import TestCase
from django.urls import reverse
from django.test import override_settings

from .factories import (
    UserFactory,
    CustomerFactory,
    UserProfileFactory,
)
from ..models import Customer

tz = pytz.timezone("Europe/Ljubljana")


@override_settings(LANGUAGE_CODE="en-US")
class CustomerTest(TestCase):
    def test_customer_add(self):
        therapist = UserProfileFactory().user
        self.client.force_login(therapist)
        data = {
            "name": "Bozo",
            "surname": "Novak",
            "email": "bozo@example.com",
            "phone": "041 123 456",
            "occupation": "na",
            "salon_choice": "na",
            "frequency": "na",
            "referral": "na",
        }

        response = self.client.post(
            path=reverse("customer_add"), data=data, follow=True
        )

        customer = Customer.objects.latest("pk")
        self.assertEqual(customer.phone, data["phone"])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="Bozo")

    def test_customer_no_duplication(self):
        therapist = UserFactory()
        self.client.force_login(therapist)
        data = {
            "name": "Bozo",
            "surname": "Novak",
            "email": "bozo@example.com",
            "phone": "041 123 456",
            "occupation": "na",
            "salon_choice": "na",
            "frequency": "na",
            "referral": "na",
        }

        response = self.client.post(
            path=reverse("customer_add"), data=data, follow=True
        )

        customer = Customer.objects.latest("pk")
        self.assertEqual(customer.phone, data["phone"])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="Bozo")

        data2 = {
            "name": "Bozo",
            "surname": "Novak",
            "email": "bozo@example.com",
            "phone": "041 123 456",
            "occupation": "na",
            "salon_choice": "na",
            "frequency": "na",
            "referral": "na",
        }

        response = self.client.post(path=reverse("customer_add"), data=data2)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="Customer already exists in database")

    def test_new_customer_displays(self):
        """
        The main_concern column to the Customer model was added after the `add_customer` button was removed.
        The edit main_concern column is tested in `test_customer_edit_main_concern`.
        """
        therapist = UserProfileFactory(external_id="42").user
        self.client.force_login(therapist)
        data = {
            "name": "Bozo",
            "surname": "Novak",
            "email": "bozo@example.com",
            "phone": "041 123 456",
            "occupation": "na",
            "salon_choice": "na",
            "frequency": "na",
            "referral": "na",
            "main_concern": "car accident",
        }

        response = self.client.post(reverse("customer_add"), data=data, follow=True)

        customer = Customer.objects.latest("pk")
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response, reverse("customer", kwargs={"customer_pk": customer.pk})
        )
        self.assertContains(response, text="Bozo")
        self.assertContains(response, text="car accident")

    def test_customer_edit(self):
        therapist = UserFactory()
        self.client.force_login(therapist)
        customer = CustomerFactory(occupation="florist", referral="from friend")

        data = {
            "name": customer.name,
            "surname": customer.surname,
            "email": customer.email,
            "phone": customer.phone,
            "occupation": customer.occupation,
            "salon_choice": customer.salon_choice,
            "frequency": customer.frequency,
            "referral": customer.referral,
        }

        # create customer

        response = self.client.get(
            reverse("customer_edit", kwargs={"customer_pk": customer.pk})
        )
        self.assertContains(response, text="from friend")
        self.assertContains(response, text="florist")

        # edit customer
        data["occupation"] = "programmer"
        response = self.client.post(
            reverse("customer_edit", kwargs={"customer_pk": customer.pk}), data=data
        )

        # assert that the occupation changed to programmer
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("customer", kwargs={"customer_pk": customer.pk})
        )
        response = self.client.get(response.url)
        self.assertContains(response, text="programmer")
        # assert from db that the occupation is programmer
        customer.refresh_from_db()
        self.assertEqual(customer.occupation, "programmer")

    def test_customer_edit_main_concern(self):
        therapist = UserFactory()
        self.client.force_login(therapist)
        customer = CustomerFactory(main_concern="car accident")

        data = {
            "name": customer.name,
            "surname": customer.surname,
            "email": customer.email,
            "phone": customer.phone,
            "occupation": customer.occupation,
            "salon_choice": customer.salon_choice,
            "frequency": customer.frequency,
            "referral": customer.referral,
            "main_concern": customer.main_concern,
        }

        # create customer
        response = self.client.get(
            reverse("customer_edit", kwargs={"customer_pk": customer.pk})
        )
        self.assertContains(response, text="car accident")

        # edit customer
        data["main_concern"] = "bike accident"
        response = self.client.post(
            reverse("customer_edit", kwargs={"customer_pk": customer.pk}), data=data
        )

        # assert that the main_concern changed to "bike accident"
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("customer", kwargs={"customer_pk": customer.pk})
        )
        response = self.client.get(response.url)
        self.assertContains(response, text="bike accident")
        # assert from db that the main concern is "bike accident"
        customer.refresh_from_db()
        self.assertEqual(customer.main_concern, "bike accident")

    def test_search_customer_list(self):
        therapist = UserFactory()
        self.client.force_login(therapist)
        customer1 = CustomerFactory(name="Peter", surname="Doe")
        customer2 = CustomerFactory(name="Rebeca", surname="O'Sullivan")
        customer3 = CustomerFactory(name="Petra", surname="Dunkirk")

        q = "P"

        response = self.client.get(reverse("customer_list") + f"?q={q}")

        """
        Because of search param "P". list should contain names "Peter" and "Petra" and not "Rebeca".
        """
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Peter")
        self.assertContains(response, "Petra")
        self.assertNotContains(response, "Rebeca")
        self.assertNotContains(response, "O'Sullivan")
