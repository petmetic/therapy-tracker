from django.test import TestCase
from django.urls import reverse

from .factories import UserFactory, CustomerFactory
from .models import Massage, Customer


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
        self.assertContains(response, text="Please log in to see Alenka masaže.")

    def test_homepage_loads(self):  # therapist already logged in
        therapist = UserFactory()
        self.client.force_login(therapist)
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="Today's massage:")

    def test_check_listing_views(self):
        pass

    def test_check_access_permission(self):
        pass


class CustomerTest(TestCase):
    def test_customer_add(self):
        therapist = UserFactory()
        self.client.force_login(therapist)
        data = {
            "name": ["Bozo"],
            "surname": ["Novak"],
            "email": ["bozo@example.com"],
            "phone": ["041 123 456"],
            "occupation": ["na"],
            "salon_choice": ["na"],
            "frequency": ["na"],
            "referral": ["na"],
        }

        response = self.client.post(
            path=reverse("customer_add"), data=data, follow=True
        )
        print(response.content)

        customer = Customer.objects.latest("pk")
        self.assertEqual([customer.phone], data["phone"])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="Bozo")

    def test_customer_no_duplication(self):
        therapist = UserFactory()
        self.client.force_login(therapist)
        data = {
            "name": ["Bozo"],
            "surname": ["Novak"],
            "email": ["bozo@example.com"],
            "phone": ["041 123 456"],
            "occupation": ["na"],
            "salon_choice": ["na"],
            "frequency": ["na"],
            "referral": ["na"],
        }

        response = self.client.post(
            path=reverse("customer_add"), data=data, follow=True
        )

        customer = Customer.objects.latest("pk")
        self.assertEqual([customer.phone], data["phone"])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="Bozo")

        data2 = {
            "name": ["Bozo"],
            "surname": ["Novak"],
            "email": ["bozo@example.com"],
            "phone": ["041 123 456"],
            "occupation": ["na"],
            "salon_choice": ["na"],
            "frequency": ["na"],
            "referral": ["na"],
        }

        response = self.client.post(path=reverse("customer_add"), data=data2)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="Customer already exists in database")


class MassageTest(TestCase):
    def test_submit_add_massage(self):  # therapist already logged in
        therapist = UserFactory()
        self.client.force_login(therapist)  # logs in the user
        customer = CustomerFactory(email="test@example.com")
        data = {
            "customer": [customer.id],
            "therapist": [therapist.id],
            "massage_date": ["2023-04-12"],
            "reason_for_visit": ["ali deluje"],
            "kind": ["terapevtska"],
            "massage_notes": ["gremo naprej"],
            "next_visit": ["hahaha"],
            "recommendations": [""],
            "personal_notes": [""],
            "duration": ["30 min"],
            "amount": ["45"],
            "discount": ["30 %"],
            "discount_reason": ["kar tako"],
            "repeat_visit": ["on"],
        }

        response = self.client.post(
            reverse("massage_add", kwargs={"customer_pk": customer.pk}), data=data
        )
        massage = Massage.objects.latest("id")

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("massage_detail", kwargs={"pk": massage.pk})
        )
