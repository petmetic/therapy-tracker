from django.test import TestCase
from django.urls import reverse

from .factories import UserFactory, CustomerFactory
from .models import Massage


class IndexTest(TestCase):
    def test_homepage_loads(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="Today's massage:")

    def test_submit_new_massage(self):
        therapist = UserFactory()
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

    def test_check_listing_views(self):
        pass

    def check_access_permission(self):
        pass


# TODO: factories to create customers, therapists(users) and therapies
