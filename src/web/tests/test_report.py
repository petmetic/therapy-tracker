import datetime
import pytz


from django.test import TestCase
from django.urls import reverse
from django.test import override_settings

from .factories import (
    UserFactory,
    CustomerFactory,
    MassageFactory,
    UserProfileFactory,
)
from ..models import Massage

tz = pytz.timezone("Europe/Ljubljana")


@override_settings(LANGUAGE_CODE="en-US")
class ReportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_reports(self):
        therapist = UserFactory()
        self.client.force_login(therapist)
        customer = CustomerFactory(email="test@example.com")
        data = {
            "customer": customer.id,
            "therapist": therapist.id,
            "start": "2023-04-12 15:00:00",
            "reason_for_visit": "pain",
            "kind": "therapeutic",
            "notes": "continue massage at home",
            "next_visit": "in 14 days",
            "recommendations": "",
            "personal_notes": "",
            "duration": 30,
            "amount": 6,
            "discount": 30,
            "discount_reason": "friend",
            "repeat_visit": "on",
        }

        response = self.client.post(
            reverse("massage_add", kwargs={"customer_pk": customer.pk}), data=data
        )
        massage = Massage.objects.latest("id")

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("massage_detail", kwargs={"pk": massage.pk})
        )
        response = self.client.get(response.url)
        self.assertContains(response, text="friend")
