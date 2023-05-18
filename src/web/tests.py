import datetime
import pytz

from django.test import TestCase
from django.urls import reverse

from .factories import UserFactory, CustomerFactory, MassageFactory, UserProfileFactory
from .models import Massage, Customer, User, Service
from .utility import therapist_import, services_import, customer_import, massage_import


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
        self.assertContains(response, text="Appointments for")

    def test_check_listing_views(self):
        pass

    def test_check_access_permission(self):
        pass


class CustomerTest(TestCase):
    def test_customer_add(self):
        therapist = UserProfileFactory().user
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
        self.assertEqual(customer.phone, data["phone"][0])
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
        self.assertEqual(customer.phone, data["phone"][0])
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

    def test_new_customer_displays(self):
        therapist = UserProfileFactory(external_id="42").user
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

        response = self.client.post(reverse("customer_add"), data=data, follow=True)

        customer = Customer.objects.latest("pk")
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response, reverse("customer", kwargs={"customer_pk": customer.pk})
        )
        self.assertContains(response, text="Bozo")

    def test_customer_edit(self):
        therapist = UserFactory()
        self.client.force_login(therapist)
        customer = CustomerFactory(occupation="florist", referral="from friend")

        data = {
            "name": [customer.name],
            "surname": [customer.surname],
            "email": [customer.email],
            "phone": [customer.phone],
            "occupation": [customer.occupation],
            "salon_choice": [customer.salon_choice],
            "frequency": [customer.frequency],
            "referral": [customer.referral],
        }

        # create customer

        response = self.client.get(
            reverse("customer_edit", kwargs={"customer_pk": customer.pk})
        )
        self.assertContains(response, text="from friend")
        self.assertContains(response, text="florist")

        # edit customer
        data["occupation"] = ["programmer"]
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


class MassageTest(TestCase):
    def test_submit_add_massage(self):  # therapist already logged in
        therapist = UserFactory()
        self.client.force_login(therapist)  # logs in the user
        customer = CustomerFactory(email="test@example.com")
        data = {
            "customer": [customer.id],
            "therapist": [therapist.id],
            "start": ["2023-04-12 15:00:00"],
            "reason_for_visit": ["pain"],
            "kind": ["therapeutic"],
            "notes": ["continue massage at home"],
            "next_visit": ["in 14 days"],
            "recommendations": [""],
            "personal_notes": [""],
            "duration": [30],
            "amount": [6],
            "discount": [30],
            "discount_reason": ["friend"],
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
        response = self.client.get(response.url)
        self.assertContains(response, text="friend")

    def test_edit_submitted_massage(self):
        therapist = UserFactory()
        self.client.force_login(therapist)  # logs in the user
        customer = CustomerFactory(email="test@example.com")

        data = {
            "customer": [customer.id],
            "therapist": [therapist.id],
            "start": ["2023-04-12 15:00:00"],
            "reason_for_visit": ["pain"],
            "kind": ["therapeutic"],
            "notes": ["continue massage at home"],
            "next_visit": ["in 14 days"],
            "recommendations": [""],
            "personal_notes": [""],
            "duration": [30],
            "amount": [7],
            "discount": [30],
            "discount_reason": ["friend"],
            "repeat_visit": ["on"],
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

    def test_discount_reason_not_filled(self):
        therapist = UserFactory()
        self.client.force_login(therapist)
        customer = CustomerFactory()
        data = {
            "customer": [customer.id],
            "therapist": [therapist.id],
            "date": ["2023-04-12"],
            "start": ["2023-04-12 15:00:00"],
            "reason_for_visit": ["pain"],
            "kind": ["therapeutic"],
            "notes": ["continue massage at home"],
            "next_visit": ["in 14 days"],
            "recommendations": [""],
            "personal_notes": [""],
            "duration": [30],
            "amount": [6],
            "discount": [20],
            "discount_reason": [""],
            "repeat_visit": ["on"],
        }

        response = self.client.post(
            reverse("massage_add", kwargs={"customer_pk": customer.pk}), data=data
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="Please fill in")

        # added discount reason
        data["discount_reason"] = ["friend"]

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


class ImportDataTest(TestCase):
    def test_therapist_import(self):
        data = {
            "message": "Successfully retrieved entities",
            "data": {
                "employees": [
                    {
                        "id": 7,
                        "firstName": "Anja",
                        "lastName": "Novak",
                        "email": "anja@example.com",
                        "phone": "+386",
                    },
                    {
                        "id": 17,
                        "firstName": "Blaz",
                        "lastName": "",
                        "email": "example@alenka-masaze.si",
                    },
                ],
            },
        }
        user_count = User.objects.all().count()
        therapist_import(data)

        self.assertEqual(User.objects.all().count(), user_count + 2)

        user = User.objects.latest("id")

        self.assertEqual(user.first_name, "Blaz")
        self.assertEqual(user.email, "example@alenka-masaze.si")
        self.assertEqual(int(user.userprofile.external_id), 17)

    def test_services_import(self):
        data = {
            "message": "Successfully retrieved entities",
            "data": {
                "categories": [
                    {
                        "id": 21,
                        "status": "visible",
                        "name": "Individualne masa\u017ee",
                        "serviceList": [
                            {
                                "id": 23,
                                "name": "Masa\u017ea 25 min",
                                "price": 5,
                                "deposit": 0,
                                "position": 6,
                                "duration": 1800,
                                "timeBefore": None,
                                "timeAfter": None,
                            },
                            {
                                "id": 29,
                                "name": "Masa\u017ea 50 minut",
                                "price": 1,
                                "duration": 3600,
                                "timeBefore": None,
                                "timeAfter": None,
                            },
                        ],
                    },
                    {
                        "id": 22,
                        "status": "visible",
                        "name": "Masa\u017ee za pare",
                        "serviceList": [
                            {
                                "id": 25,
                                "name": "Spro\u0161\u010dujo\u010da masa\u017ea 50 min",
                                "price": 3,
                                "duration": 4800,
                                "timeBefore": 600,
                                "timeAfter": None,
                            },
                            {
                                "id": 26,
                                "name": "Spro\u0161\u010dujo\u010da masa\u017ea 80 min",
                                "price": 7,
                                "duration": 6600,
                                "timeBefore": 600,
                                "timeAfter": None,
                            },
                        ],
                        "position": 2,
                        "translations": None,
                    },
                    {
                        "id": 26,
                        "status": "visible",
                        "name": "Limfna drena\u017ea",
                        "serviceList": [
                            {
                                "id": 27,
                                "name": "Limfna drena\u017ea 50 min",
                                "price": 13,
                                "duration": 3600,
                                "timeBefore": None,
                                "timeAfter": None,
                            }
                        ],
                        "position": 3,
                        "translations": None,
                    },
                ],
            },
        }

        service_count = Service.objects.all().count()
        services_import(data)

        self.assertEqual(Service.objects.all().count(), service_count + 5)

        service = Service.objects.latest("id")

        self.assertEqual(service.service_group, "Limfna drena\u017ea")
        self.assertEqual(service.name, "Limfna drena\u017ea 50 min")
        self.assertEqual(service.external_id, 27)
        self.assertEqual(service.price, 13)
        self.assertEqual(service.duration, 3600)
        self.assertEqual(service.time_before, 0)
        self.assertEqual(service.time_after, 0)

    def test_customer_import(self):
        data = {
            "message": "Successfully retrieved appointments",
            "data": {
                "appointments": {
                    "2023-06-07": {
                        "date": "2023-06-07",
                        "appointments": [
                            {
                                "id": 576,
                                "bookings": [
                                    {
                                        "id": 345,
                                        "customerId": 333,
                                        "customer": {
                                            "id": 333,
                                            "firstName": "Example",
                                            "lastName": "Example",
                                            "email": "example@gmail.com",
                                            "phone": "+3841123123",
                                        },
                                        "status": "approved",
                                        "price": 50,
                                        "appointmentId": 576,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": "approved",
                                "serviceId": 7,
                                "providerId": 1,
                                "bookingStart": "2023-04-06 16:00:00",
                                "bookingEnd": "2023-04-06 17:00:00",
                            },
                        ],
                    },
                    "2023-05-05": {
                        "date": "2023-05-05",
                        "appointments": [
                            {
                                "id": 555,
                                "bookings": [
                                    {
                                        "id": 270,
                                        "customerId": 41,
                                        "customer": {
                                            "id": 41,
                                            "firstName": "Maja",
                                            "lastName": "Novak",
                                            "birthday": None,
                                            "email": None,
                                            "phone": "+38641123123",
                                        },
                                        "status": "approved",
                                        "price": 70,
                                        "appointmentId": 555,
                                        "persons": 1,
                                        "duration": 5400,
                                        "created": "2023-04-4 09:20:20",
                                    }
                                ],
                                "status": "approved",
                                "serviceId": 3,
                                "providerId": 1,
                                "bookingStart": "2023-04-07 09:00:00",
                                "bookingEnd": "2023-04-07 10:30:00",
                            },
                        ],
                    },
                },
            },
        }

        customer_count = Customer.objects.all().count()
        customer_import(data)

        self.assertEqual(Customer.objects.all().count(), customer_count + 2)

        customer = Customer.objects.latest("id")

        self.assertEqual(customer.name, "Maja")
        self.assertEqual(customer.surname, "Novak")
        self.assertEqual(customer.external_id, "41")

    def test_massage_import(self):
        data = {
            "message": "Successfully retrieved appointments",
            "data": {
                "appointments": {
                    "2023-06-07": {
                        "date": "2023-06-07",
                        "appointments": [
                            {
                                "id": 576,
                                "bookings": [
                                    {
                                        "id": 345,
                                        "customerId": 333,
                                        "customer": {
                                            "id": 333,
                                            "firstName": "Example",
                                            "lastName": "Example",
                                            "email": "example@gmail.com",
                                            "phone": "+3841123123",
                                        },
                                        "status": "approved",
                                        "price": 50,
                                        "appointmentId": 576,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": "approved",
                                "serviceId": 7,
                                "providerId": 42,
                                "bookingStart": "2023-04-06 16:00:00",
                                "bookingEnd": "2023-04-06 17:00:00",
                            },
                        ],
                    },
                    "2023-05-05": {
                        "date": "2023-05-05",
                        "appointments": [
                            {
                                "id": 555,
                                "bookings": [
                                    {
                                        "id": 270,
                                        "customerId": 41,
                                        "customer": {
                                            "id": 41,
                                            "firstName": "Maja",
                                            "lastName": "Novak",
                                            "birthday": None,
                                            "email": None,
                                            "phone": "+38641123123",
                                        },
                                        "status": "approved",
                                        "price": 70,
                                        "appointmentId": 555,
                                        "persons": 1,
                                        "duration": 5400,
                                        "created": "2023-04-4 09:20:20",
                                    }
                                ],
                                "status": "approved",
                                "serviceId": 3,
                                "providerId": 42,
                                "bookingStart": "2023-04-07 09:00:00",
                                "bookingEnd": "2023-04-07 10:30:00",
                            },
                        ],
                    },
                },
            },
        }

        UserProfileFactory(external_id="42")

        massage_count = Massage.objects.all().count()

        massage_import(data)

        self.assertEqual(Massage.objects.all().count(), massage_count + 2)

        massage = Massage.objects.latest("id")
        self.assertEqual(massage.external_id, 270)

        tz = pytz.timezone("Europe/Berlin")
        expected_date = datetime.datetime(2023, 4, 7, 9, 0)
        expected_date = tz.localize(expected_date)

        self.assertEqual(
            massage.start.astimezone(tz).isoformat(), expected_date.isoformat()
        )
