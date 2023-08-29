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
class MassageTest(TestCase):
    def test_submit_add_massage(self):  # therapist already logged in
        therapist = UserFactory()
        self.client.force_login(therapist)  # logs in the user
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

    def test_edit_submitted_massage(self):
        therapist = UserFactory()
        self.client.force_login(therapist)  # logs in the user
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
            "amount": 7,
            "discount": 30,
            "discount_reason": "friend",
            "repeat_visit": "on",
        }

        # add new massage
        response = self.client.post(
            reverse("massage_add", kwargs={"customer_pk": customer.pk}), data=data
        )

        massage = Massage.objects.latest("id")

        self.assertRedirects(
            response, reverse("massage_detail", kwargs={"pk": massage.pk})
        )

        # edit massage
        response = self.client.get(reverse("massage_edit", kwargs={"pk": massage.pk}))
        self.assertContains(response, text="pain")
        data["reason_for_visit"] = ["PAIN"]

        response = self.client.post(
            reverse("massage_edit", kwargs={"pk": massage.pk}), data=data
        )

        # assert
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("massage_detail", kwargs={"pk": massage.pk})
        )
        response = self.client.get(response.url)
        self.assertContains(response, text="PAIN")

    def test_edit_main_concern_in_edit_massage_view(self):
        therapist = UserProfileFactory(user__first_name="Jane").user
        self.client.force_login(therapist)
        customer = CustomerFactory(name="Brian", main_concern="car accident")

        massage = MassageFactory(
            therapist=therapist,
            customer=customer,
            start=datetime.datetime(2023, 4, 6, 16, 0, 0).astimezone(tz=tz),
            status="approved",
        )

        data = {
            "customer": customer.id,
            "therapist": therapist.id,
            "start": massage.start,
            "reason_for_visit": "pain",
            "kind": "therapeutic",
            "notes": "continue massage at home",
            "next_visit": "in 14 days",
            "recommendations": "",
            "personal_notes": "",
            "duration": 30,
            "amount": 7,
            "discount": 30,
            "discount_reason": "friend",
            "repeat_visit": "on",
            "main_concern": customer.main_concern,
        }

        response = self.client.post(
            reverse("massage_add", kwargs={"customer_pk": customer.pk}), data=data
        )
        self.assertEqual(response.status_code, 302)

        massage = Massage.objects.latest("id")

        response = self.client.get(reverse("massage_edit", kwargs={"pk": massage.pk}))
        self.assertContains(response, "2023-04-06 16:00:00")
        self.assertContains(response, text="car accident")
        data["main_concern"] = "bike accident"

        response = self.client.post(
            reverse("massage_edit", kwargs={"pk": massage.pk}), data=data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("massage_detail", kwargs={"pk": massage.pk})
        )
        response = self.client.get(response.url)
        self.assertContains(response, text="bike accident")

    def test_discount_reason_not_filled(self):
        therapist = UserFactory()
        self.client.force_login(therapist)
        customer = CustomerFactory()
        data = {
            "customer": customer.id,
            "therapist": therapist.id,
            "date": "2023-04-12",
            "start": "2023-04-12 15:00:00",
            "reason_for_visit": "pain",
            "kind": "therapeutic",
            "notes": "continue massage at home",
            "next_visit": "in 14 days",
            "recommendations": "",
            "personal_notes": "",
            "duration": 30,
            "amount": 6,
            "discount": 20,
            "discount_reason": "",
            "repeat_visit": "on",
        }

        response = self.client.post(
            reverse("massage_add", kwargs={"customer_pk": customer.pk}), data=data
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="Please fill in")

        # added discount reason
        data["discount_reason"] = "friend"

        response = self.client.post(
            reverse("massage_add", kwargs={"customer_pk": customer.pk}), data=data
        )

        massage = Massage.objects.latest("id")

        # assert discount reason is filled
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("massage_detail", kwargs={"pk": massage.pk})
        )
        response = self.client.get(response.url)
        self.assertContains(response, text="friend")

    def test_massage_display(self):
        therapist = UserFactory()
        self.client.force_login(therapist)
        customer = CustomerFactory()
        massage = MassageFactory(
            customer=customer, therapist=therapist, personal_notes="TEST?"
        )

        response = self.client.get(reverse("massage_detail", kwargs={"pk": massage.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="TEST?")

    def test_personal_notes_display(self):
        therapist = UserFactory()
        self.client.force_login(therapist)
        customer = CustomerFactory()
        massage = MassageFactory(
            customer=customer, therapist=therapist, personal_notes="TEST?"
        )

        response = self.client.get(reverse("massage_detail", kwargs={"pk": massage.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="TEST?")

        self.client.logout()
        therapist2 = UserFactory()
        self.client.force_login(therapist2)
        customer = CustomerFactory()
        massage = MassageFactory(
            customer=customer, therapist=therapist, personal_notes="TEST?"
        )

        response = self.client.get(reverse("massage_detail", kwargs={"pk": massage.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, text="TEST?")

    def test_user1_sees_massage_from_user2(self):
        therapist1 = UserFactory()
        therapist2 = UserFactory()
        customer = CustomerFactory()

        self.client.force_login(therapist1)
        massage = MassageFactory(
            customer=customer,
            therapist=therapist1,
            notes="anti inflammatory massage of knee",
        )
        response = self.client.get(reverse("massage_detail", kwargs={"pk": massage.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="anti inflammatory massage of knee")

        # therapist2 tries to edit massage_detail.html and edit button is not displayed
        self.client.logout()
        self.client.force_login(therapist2)
        response = self.client.get(reverse("massage_detail", kwargs={"pk": massage.pk}))
        self.assertNotContains(response, text="Edit massage")

        # therapist2 tries to edit massage_edit.html and fails
        response = self.client.get(reverse("massage_edit", kwargs={"pk": massage.pk}))
        self.assertEqual(response.status_code, 403)
