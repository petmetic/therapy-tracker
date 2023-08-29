import datetime
import pytz
from freezegun import freeze_time

from django.test import TestCase
from django.urls import reverse
from django.test import override_settings

from .factories import (
    UserFactory,
    CustomerFactory,
    MassageFactory,
    UserProfileFactory,
    ServiceFactory,
)
from .models import Massage, Customer, User, Service
from .importer import (
    therapist_import,
    services_import,
    customer_import,
    massage_import,
    update_or_create_w_logging,
    single_massage_import,
    massage_appointments,
    massage_date_comparison_with_wp_db,
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

        massage1 = MassageFactory(
            therapist=therapist1,
            customer=customer1,
            start=datetime.datetime(2023, 4, 6, 16, 0, 0).astimezone(tz=tz),
            status="approved",
        )
        massage2 = MassageFactory(
            therapist=therapist1,
            customer=customer2,
            start=datetime.datetime(2023, 4, 6, 18, 0, 0).astimezone(tz=tz),
            status="canceled",
        )
        massage3 = MassageFactory(
            therapist=therapist1,
            customer=customer3,
            start=datetime.datetime(2023, 4, 7, 17, 0, 0).astimezone(tz=tz),
        )
        massage4 = MassageFactory(
            therapist=therapist1,
            customer=customer4,
            start=datetime.datetime(2023, 4, 5, 17, 0, 0).astimezone(tz=tz),
        )
        massage5 = MassageFactory(
            therapist=therapist2,
            customer=customer5,
            start=datetime.datetime(2023, 4, 6, 19, 0, 0).astimezone(tz=tz),
        )
        massage6 = MassageFactory(
            therapist=therapist2,
            customer=customer6,
            start=datetime.datetime(2023, 4, 4, 19, 0, 0).astimezone(tz=tz),
        )

        data = {
            "message": "Successfully retrieved appointments",
            "data": {
                "appointments": {
                    "2023-04-06": {
                        "date": "2023-04-06",
                        "appointments": [
                            {
                                "id": 576,
                                "bookings": [
                                    {
                                        "id": 345,
                                        "customerId": 333,
                                        "customer": {
                                            "id": customer1.external_id,
                                            "firstName": customer1.name,
                                            "lastName": customer1.surname,
                                            "email": customer1.email,
                                            "phone": customer1.phone,
                                        },
                                        "status": massage1.status,
                                        "price": massage1.service.price,
                                        "appointmentId": massage1.external_id,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": massage1.status,
                                "serviceId": massage1.service.external_id,
                                "providerId": massage1.therapist.userprofile.external_id,
                                "bookingStart": massage1.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage1.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            },
                            {
                                "id": 577,
                                "bookings": [
                                    {
                                        "id": 345,
                                        "customerId": 333,
                                        "customer": {
                                            "id": customer2.external_id,
                                            "firstName": customer2.name,
                                            "lastName": customer2.surname,
                                            "email": customer2.email,
                                            "phone": customer2.phone,
                                        },
                                        "status": massage2.status,
                                        "price": massage2.service.price,
                                        "appointmentId": massage2.external_id,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": massage2.status,
                                "serviceId": massage2.service.external_id,
                                "providerId": massage2.therapist.userprofile.external_id,
                                "bookingStart": massage2.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage2.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            },
                            {
                                "id": 578,
                                "bookings": [
                                    {
                                        "id": 345,
                                        "customerId": 333,
                                        "customer": {
                                            "id": customer5.external_id,
                                            "firstName": customer5.name,
                                            "lastName": customer5.surname,
                                            "email": customer5.email,
                                            "phone": customer5.phone,
                                        },
                                        "status": massage5.status,
                                        "price": massage5.service.price,
                                        "appointmentId": massage5.external_id,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": massage5.status,
                                "serviceId": massage5.service.external_id,
                                "providerId": massage5.therapist.userprofile.external_id,
                                "bookingStart": massage5.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage5.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            },
                        ],
                    },
                    "2023-04-07": {
                        "date": "2023-04-07",
                        "appointments": [
                            {
                                "id": 579,
                                "bookings": [
                                    {
                                        "id": 345,
                                        "customerId": 333,
                                        "customer": {
                                            "id": customer3.external_id,
                                            "firstName": customer3.name,
                                            "lastName": customer3.surname,
                                            "email": customer3.email,
                                            "phone": customer3.phone,
                                        },
                                        "status": massage3.status,
                                        "price": massage3.service.price,
                                        "appointmentId": massage3.external_id,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": massage3.status,
                                "serviceId": massage3.service.external_id,
                                "providerId": massage3.therapist.userprofile.external_id,
                                "bookingStart": massage3.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage3.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            },
                        ],
                    },
                    "2023-04-05": {
                        "date": "2023-04-05",
                        "appointments": [
                            {
                                "id": 580,
                                "bookings": [
                                    {
                                        "id": 345,
                                        "customerId": 333,
                                        "customer": {
                                            "id": customer4.external_id,
                                            "firstName": customer4.name,
                                            "lastName": customer4.surname,
                                            "email": customer4.email,
                                            "phone": customer4.phone,
                                        },
                                        "status": massage4.status,
                                        "price": massage4.service.price,
                                        "appointmentId": massage4.external_id,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": massage4.status,
                                "serviceId": massage4.service.external_id,
                                "providerId": massage4.therapist.userprofile.external_id,
                                "bookingStart": massage4.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage4.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            },
                        ],
                    },
                    "2023-04-04": {
                        "date": "2023-04-05",
                        "appointments": [
                            {
                                "id": 581,
                                "bookings": [
                                    {
                                        "id": 345,
                                        "customerId": 333,
                                        "customer": {
                                            "id": customer6.external_id,
                                            "firstName": customer6.name,
                                            "lastName": customer6.surname,
                                            "email": customer6.email,
                                            "phone": customer6.phone,
                                        },
                                        "status": massage6.status,
                                        "price": massage6.service.price,
                                        "appointmentId": massage6.external_id,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": massage6.status,
                                "serviceId": massage6.service.external_id,
                                "providerId": massage6.therapist.userprofile.external_id,
                                "bookingStart": massage6.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage6.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            },
                        ],
                    },
                },
            },
        }

        customer_import(data)
        massage_import(data)
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

        massage1 = MassageFactory(
            therapist=therapist1,
            customer=customer1,
            start=datetime.datetime(2023, 4, 6, 16, 0, 0).astimezone(tz=tz),
            status="approved",
        )
        massage2 = MassageFactory(
            therapist=therapist1,
            customer=customer2,
            start=datetime.datetime(2023, 4, 6, 18, 0, 0).astimezone(tz=tz),
            status="canceled",
        )
        massage3 = MassageFactory(
            therapist=therapist1,
            customer=customer3,
            start=datetime.datetime(2023, 4, 7, 17, 0, 0).astimezone(tz=tz),
            status="approved",
        )

        data = {
            "message": "Successfully retrieved appointments",
            "data": {
                "appointments": {
                    "2023-04-06": {
                        "date": "2023-04-06",
                        "appointments": [
                            {
                                "id": 576,
                                "bookings": [
                                    {
                                        "id": 345,
                                        "customerId": 333,
                                        "customer": {
                                            "id": customer1.external_id,
                                            "firstName": customer1.name,
                                            "lastName": customer1.surname,
                                            "email": customer1.email,
                                            "phone": customer1.phone,
                                        },
                                        "status": massage1.status,
                                        "price": massage1.service.price,
                                        "appointmentId": massage1.external_id,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": massage1.status,
                                "serviceId": massage1.service.external_id,
                                "providerId": massage1.therapist.userprofile.external_id,
                                "bookingStart": massage1.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage1.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            },
                            {
                                "id": 577,
                                "bookings": [
                                    {
                                        "id": 345,
                                        "customerId": 333,
                                        "customer": {
                                            "id": customer2.external_id,
                                            "firstName": customer2.name,
                                            "lastName": customer2.surname,
                                            "email": customer2.email,
                                            "phone": customer2.phone,
                                        },
                                        "status": massage2.status,
                                        "price": massage2.service.price,
                                        "appointmentId": massage2.external_id,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": massage2.status,
                                "serviceId": massage2.service.external_id,
                                "providerId": massage2.therapist.userprofile.external_id,
                                "bookingStart": massage2.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage2.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            },
                        ],
                    },
                    "2023-04-07": {
                        "date": "2023-04-07",
                        "appointments": [
                            {
                                "id": 579,
                                "bookings": [
                                    {
                                        "id": 345,
                                        "customerId": 333,
                                        "customer": {
                                            "id": customer3.external_id,
                                            "firstName": customer3.name,
                                            "lastName": customer3.surname,
                                            "email": customer3.email,
                                            "phone": customer3.phone,
                                        },
                                        "status": massage3.status,
                                        "price": massage3.service.price,
                                        "appointmentId": massage3.external_id,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": massage3.status,
                                "serviceId": massage3.service.external_id,
                                "providerId": massage3.therapist.userprofile.external_id,
                                "bookingStart": massage3.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage3.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            },
                        ],
                    },
                },
            },
        }

        customer_import(data)
        massage_import(data)
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
        # name of customer displays
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

    def test_therapist_update(self):
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

        # changed email of first user, changed first name of second user
        data2 = {
            "message": "Successfully retrieved entities",
            "data": {
                "employees": [
                    {
                        "id": 7,
                        "firstName": "Anja",
                        "lastName": "Novak",
                        "email": "novak@example.com",
                        "phone": "+386",
                    },
                    {
                        "id": 17,
                        "firstName": "Anamarija",
                        "lastName": "",
                        "email": "example@alenka-masaze.si",
                    },
                ],
            },
        }

        user_count1 = User.objects.all().count()

        therapist_import(data)

        self.assertEqual(User.objects.all().count(), user_count1 + 2)

        user = User.objects.latest("id")
        self.assertEqual(user.first_name, "Blaz")
        self.assertEqual(user.email, "example@alenka-masaze.si")

        user = User.objects.get(userprofile__external_id=7)
        self.assertEqual(user.first_name, "Anja")
        self.assertEqual(user.email, "anja@example.com")

        user_count2 = User.objects.all().count()

        therapist_import(data2)

        self.assertEqual(User.objects.all().count(), user_count2)

        user = User.objects.latest("id")
        self.assertEqual(user.first_name, "Anamarija")
        self.assertEqual(user.email, "example@alenka-masaze.si")
        self.assertEqual(int(user.userprofile.external_id), 17)

        user = User.objects.get(userprofile__external_id=7)
        self.assertEqual(user.first_name, "Anja")
        self.assertEqual(user.email, "novak@example.com")

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
        therapist = UserProfileFactory()
        massage1 = MassageFactory.build()  # do not save into db
        massage2 = MassageFactory.build(
            external_id=270, start=datetime.datetime(2023, 4, 7, 9, 0, 0)
        )
        customer1 = CustomerFactory.build()
        customer2 = CustomerFactory.build()
        service1 = ServiceFactory()
        service2 = ServiceFactory()
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
                                            "id": customer1.external_id,
                                            "firstName": customer1.name,
                                            "lastName": customer1.surname,
                                            "email": customer1.email,
                                            "phone": customer1.phone,
                                        },
                                        "status": massage1.status,
                                        "price": service1.price,
                                        "appointmentId": massage1.external_id,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": massage1.status,
                                "serviceId": service1.external_id,
                                "providerId": therapist.external_id,
                                "bookingStart": massage1.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage1.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
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
                                            "id": customer2.external_id,
                                            "firstName": customer2.name,
                                            "lastName": customer2.surname,
                                            "birthday": None,
                                            "email": customer2.email,
                                            "phone": customer2.phone,
                                        },
                                        "status": massage2.status,
                                        "price": service2.price,
                                        "appointmentId": massage2.external_id,
                                        "persons": 1,
                                        "duration": 5400,
                                        "created": "2023-04-4 09:20:20",
                                    }
                                ],
                                "status": massage2.status,
                                "serviceId": service2.external_id,
                                "providerId": therapist.external_id,
                                "bookingStart": massage2.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage2.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            },
                        ],
                    },
                },
            },
        }

        UserProfileFactory(external_id="42")

        massage_count = Massage.objects.all().count()

        customer_import(data)
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

    def test_single_massage_import(self):
        therapist = UserProfileFactory()
        massage1 = MassageFactory.build(
            external_id=30, start=datetime.datetime(2023, 5, 5, 17, 0, 0)
        )
        massage2 = MassageFactory.build(
            external_id=270, start=datetime.datetime(2023, 4, 7, 9, 0, 0)
        )
        customer1 = CustomerFactory.build()
        customer2 = CustomerFactory.build()
        service1 = ServiceFactory()
        service2 = ServiceFactory()

        data1 = {
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
                                            "id": customer1.external_id,
                                            "firstName": customer1.name,
                                            "lastName": customer1.surname,
                                            "email": customer1.email,
                                            "phone": customer1.phone,
                                        },
                                        "status": massage1.status,
                                        "price": service1.price,
                                        "appointmentId": massage1.external_id,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": massage1.status,
                                "serviceId": service1.external_id,
                                "providerId": therapist.external_id,
                                "bookingStart": massage1.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage1.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
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
                                            "id": customer2.external_id,
                                            "firstName": customer2.name,
                                            "lastName": customer2.surname,
                                            "birthday": None,
                                            "email": customer2.email,
                                            "phone": customer2.phone,
                                        },
                                        "status": massage2.status,
                                        "price": service2.price,
                                        "appointmentId": massage2.external_id,
                                        "persons": 1,
                                        "duration": 5400,
                                        "created": "2023-04-4 09:20:20",
                                    }
                                ],
                                "status": massage2.status,
                                "serviceId": service2.external_id,
                                "providerId": therapist.external_id,
                                "bookingStart": massage2.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage2.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            },
                        ],
                    },
                },
            },
        }

        # changed massage date of massage2 from 2023-04-7 at 9:00 to 2023-10-7 at 10:00
        data2 = {
            "message": "Successfully retrieved appointment",
            "data": {
                "appointment": {
                    "id": massage2.external_id,
                    "bookings": [
                        {
                            "id": 691,
                            "customerId": customer2.external_id,
                            "customer": None,
                            "status": massage2.status,
                            "price": service2.price,
                            "appointmentId": massage2.external_id,
                            "persons": 1,
                            "duration": 5400,
                            "created": "2023-04-4 09:20:20",
                        }
                    ],
                    "status": massage2.status,
                    "serviceId": service2.external_id,
                    "providerId": therapist.external_id,
                    "bookingStart": "2023-10-7 10:00:00",
                    "bookingEnd": massage2.end.strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "appointment",
                    "isRescheduled": None,
                    "isFull": None,
                    "resources": [],
                },
                "recurring": [],
            },
        }

        UserProfileFactory(external_id="42")

        massage_count = Massage.objects.all().count()

        customer_import(data1)
        massage_import(data1)

        single_massage_import(data2)

        # check that date and hour of massage1 has not changed
        massage = Massage.objects.get(external_id=30)
        tz = pytz.timezone("Europe/Berlin")
        expected_date = datetime.datetime(2023, 5, 5, 17, 0, 0)
        expected_date = tz.localize(expected_date)
        self.assertEqual(
            massage.start.astimezone(tz).isoformat(), expected_date.isoformat()
        )

        massage = Massage.objects.get(external_id=270)
        # check if massage is only changed and not added
        self.assertEqual(Massage.objects.all().count(), massage_count + 2)
        # check if start date  of massage2 is changed from 2023-04-7 at 9:00 to 2023-10-7 at 10:00
        tz = pytz.timezone("Europe/Berlin")
        expected_date = datetime.datetime(2023, 10, 7, 10, 0)
        expected_date = tz.localize(expected_date)
        self.assertEqual(
            massage.start.astimezone(tz).isoformat(), expected_date.isoformat()
        )

        # when start date is changed to future date, does it register in db
        massage = Massage.objects.latest("id")
        massage.refresh_from_db()
        self.assertEqual(massage.start, expected_date)

    def test_get_massage_appointments(self):
        """
        Get a list of external_id from the wodrpess API call
        """
        therapist1 = UserProfileFactory(user__first_name="Jane").user
        self.client.force_login(therapist1)

        customer1 = CustomerFactory(name="Brian", main_concern="car accident")
        customer2 = CustomerFactory(name="Alice", main_concern="bike accident")
        customer3 = CustomerFactory(name="David", main_concern="fall off tree")

        massage1 = MassageFactory(
            therapist=therapist1,
            customer=customer1,
            start=datetime.datetime(2023, 4, 6, 16, 0, 0).astimezone(tz=tz),
            status="approved",
            external_id=5,
        )
        massage2 = MassageFactory(
            therapist=therapist1,
            customer=customer2,
            start=datetime.datetime(2023, 4, 6, 18, 0, 0).astimezone(tz=tz),
            status="canceled",
            external_id=7,
        )
        massage3 = MassageFactory(
            therapist=therapist1,
            customer=customer3,
            start=datetime.datetime(2023, 4, 7, 17, 0, 0).astimezone(tz=tz),
            status="approved",
            external_id=8,
        )

        data = {
            "message": "Successfully retrieved appointments",
            "data": {
                "appointments": {
                    "2023-04-06": {
                        "date": "2023-04-06",
                        "appointments": [
                            {
                                "id": 576,
                                "bookings": [
                                    {
                                        "id": 345,
                                        "customerId": 333,
                                        "customer": {
                                            "id": customer1.external_id,
                                            "firstName": customer1.name,
                                            "lastName": customer1.surname,
                                            "email": customer1.email,
                                            "phone": customer1.phone,
                                        },
                                        "status": massage1.status,
                                        "price": massage1.service.price,
                                        "appointmentId": massage1.external_id,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": massage1.status,
                                "serviceId": massage1.service.external_id,
                                "providerId": massage1.therapist.userprofile.external_id,
                                "bookingStart": massage1.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage1.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            },
                            {
                                "id": 577,
                                "bookings": [
                                    {
                                        "id": 345,
                                        "customerId": 333,
                                        "customer": {
                                            "id": customer2.external_id,
                                            "firstName": customer2.name,
                                            "lastName": customer2.surname,
                                            "email": customer2.email,
                                            "phone": customer2.phone,
                                        },
                                        "status": massage2.status,
                                        "price": massage2.service.price,
                                        "appointmentId": massage2.external_id,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": massage2.status,
                                "serviceId": massage2.service.external_id,
                                "providerId": massage2.therapist.userprofile.external_id,
                                "bookingStart": massage2.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage2.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            },
                        ],
                    },
                    "2023-04-07": {
                        "date": "2023-04-07",
                        "appointments": [
                            {
                                "id": 579,
                                "bookings": [
                                    {
                                        "id": 345,
                                        "customerId": 333,
                                        "customer": {
                                            "id": customer3.external_id,
                                            "firstName": customer3.name,
                                            "lastName": customer3.surname,
                                            "email": customer3.email,
                                            "phone": customer3.phone,
                                        },
                                        "status": massage3.status,
                                        "price": massage3.service.price,
                                        "appointmentId": massage3.external_id,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": massage3.status,
                                "serviceId": massage3.service.external_id,
                                "providerId": massage3.therapist.userprofile.external_id,
                                "bookingStart": massage3.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage3.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            },
                        ],
                    },
                },
            },
        }

        massage_appointments_in_wp_db = massage_appointments(data)
        self.assertEqual(massage_appointments_in_wp_db, [5, 7, 8])

    @freeze_time("2023-04-06 13:21:34", tz_offset=2)
    def test_compare_massage_date_with_wp_db(self):
        therapist1 = UserProfileFactory(user__first_name="Jane").user
        self.client.force_login(therapist1)

        customer1 = CustomerFactory()
        customer2 = CustomerFactory()
        customer3 = CustomerFactory()
        customer4 = CustomerFactory()
        customer5 = CustomerFactory()

        massage1 = MassageFactory(
            therapist=therapist1,
            customer=customer1,
            start=datetime.datetime(2023, 4, 6, 16, 0, 0).astimezone(tz=tz),
            status="approved",
            external_id=5,
        )
        massage2 = MassageFactory(
            therapist=therapist1,
            customer=customer2,
            start=datetime.datetime(2023, 4, 6, 18, 0, 0).astimezone(tz=tz),
            status="canceled",
            external_id=7,
        )
        massage3 = MassageFactory(
            therapist=therapist1,
            customer=customer3,
            start=datetime.datetime(2023, 4, 7, 17, 0, 0).astimezone(tz=tz),
            status="approved",
            external_id=8,
        )
        massage4 = MassageFactory(
            therapist=therapist1,
            customer=customer4,
            start=datetime.datetime(2023, 4, 7, 20, 0, 0).astimezone(tz=tz),
            status="approved",
            external_id=10,
        )
        massage5 = MassageFactory(
            therapist=therapist1,
            customer=customer5,
            start=datetime.datetime(2023, 5, 17, 21, 0, 0).astimezone(tz=tz),
            status="not canceled",
            external_id=15,
        )
        # does not contain massage4(ex_id10)
        # contains massage5(ex_id15)
        data1 = {
            "message": "Successfully retrieved appointments",
            "data": {
                "appointments": {
                    "2023-04-06": {
                        "date": "2023-04-06",
                        "appointments": [
                            {
                                "id": 576,
                                "bookings": [
                                    {
                                        "id": 345,
                                        "customerId": 333,
                                        "customer": {
                                            "id": customer1.external_id,
                                            "firstName": customer1.name,
                                            "lastName": customer1.surname,
                                            "email": customer1.email,
                                            "phone": customer1.phone,
                                        },
                                        "status": massage1.status,
                                        "price": massage1.service.price,
                                        "appointmentId": massage1.external_id,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": massage1.status,
                                "serviceId": massage1.service.external_id,
                                "providerId": massage1.therapist.userprofile.external_id,
                                "bookingStart": massage1.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage1.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            },
                            {
                                "id": 577,
                                "bookings": [
                                    {
                                        "id": 345,
                                        "customerId": 333,
                                        "customer": {
                                            "id": customer2.external_id,
                                            "firstName": customer2.name,
                                            "lastName": customer2.surname,
                                            "email": customer2.email,
                                            "phone": customer2.phone,
                                        },
                                        "status": massage2.status,
                                        "price": massage2.service.price,
                                        "appointmentId": massage2.external_id,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": massage2.status,
                                "serviceId": massage2.service.external_id,
                                "providerId": massage2.therapist.userprofile.external_id,
                                "bookingStart": massage2.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage2.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            },
                        ],
                    },
                    "2023-04-07": {
                        "date": "2023-04-07",
                        "appointments": [
                            {
                                "id": 579,
                                "bookings": [
                                    {
                                        "id": 345,
                                        "customerId": 333,
                                        "customer": {
                                            "id": customer3.external_id,
                                            "firstName": customer3.name,
                                            "lastName": customer3.surname,
                                            "email": customer3.email,
                                            "phone": customer3.phone,
                                        },
                                        "status": massage3.status,
                                        "price": massage3.service.price,
                                        "appointmentId": massage3.external_id,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": massage3.status,
                                "serviceId": massage3.service.external_id,
                                "providerId": massage3.therapist.userprofile.external_id,
                                "bookingStart": massage3.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage3.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            },
                            {
                                "id": 579,
                                "bookings": [
                                    {
                                        "id": 345,
                                        "customerId": 333,
                                        "customer": {
                                            "id": customer5.external_id,
                                            "firstName": customer5.name,
                                            "lastName": customer5.surname,
                                            "email": customer5.email,
                                            "phone": customer5.phone,
                                        },
                                        "status": massage5.status,
                                        "price": massage5.service.price,
                                        "appointmentId": massage5.external_id,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": massage5.status,
                                "serviceId": massage5.service.external_id,
                                "providerId": massage5.therapist.userprofile.external_id,
                                "bookingStart": massage5.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage5.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            },
                        ],
                    },
                },
            },
        }

        # added massage4
        # does not contain massage1 and massage5
        wordpress_data = {
            "message": "Successfully retrieved appointments",
            "data": {
                "appointments": {
                    "2023-04-06": {
                        "date": "2023-04-06",
                        "appointments": [
                            {
                                "id": 577,
                                "bookings": [
                                    {
                                        "id": 345,
                                        "customerId": 333,
                                        "customer": {
                                            "id": customer2.external_id,
                                            "firstName": customer2.name,
                                            "lastName": customer2.surname,
                                            "email": customer2.email,
                                            "phone": customer2.phone,
                                        },
                                        "status": massage2.status,
                                        "price": massage2.service.price,
                                        "appointmentId": massage2.external_id,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": massage2.status,
                                "serviceId": massage2.service.external_id,
                                "providerId": massage2.therapist.userprofile.external_id,
                                "bookingStart": massage2.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage2.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            },
                        ],
                    },
                    "2023-04-07": {
                        "date": "2023-04-07",
                        "appointments": [
                            {
                                "id": 579,
                                "bookings": [
                                    {
                                        "id": 345,
                                        "customerId": 333,
                                        "customer": {
                                            "id": customer3.external_id,
                                            "firstName": customer3.name,
                                            "lastName": customer3.surname,
                                            "email": customer3.email,
                                            "phone": customer3.phone,
                                        },
                                        "status": massage3.status,
                                        "price": massage3.service.price,
                                        "appointmentId": massage3.external_id,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": massage3.status,
                                "serviceId": massage3.service.external_id,
                                "providerId": massage3.therapist.userprofile.external_id,
                                "bookingStart": massage3.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage3.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            },
                            {
                                "id": 600,
                                "bookings": [
                                    {
                                        "id": 345,
                                        "customerId": 333,
                                        "customer": {
                                            "id": customer4.external_id,
                                            "firstName": customer4.name,
                                            "lastName": customer4.surname,
                                            "email": customer4.email,
                                            "phone": customer4.phone,
                                        },
                                        "status": massage4.status,
                                        "price": massage4.service.price,
                                        "appointmentId": massage4.external_id,
                                        "persons": 1,
                                        "duration": 3600,
                                        "created": "2023-03-31 15:15:50",
                                    }
                                ],
                                "status": massage4.status,
                                "serviceId": massage4.service.external_id,
                                "providerId": massage4.therapist.userprofile.external_id,
                                "bookingStart": massage4.start.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                                "bookingEnd": massage4.end.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            },
                        ],
                    },
                },
            },
        }

        # import data1 to local db
        massage_import(data1)
        massage5 = Massage.objects.get(external_id=15)
        self.assertEqual(massage5.status, "not_canceled")

        # import wordpress_data,
        massage_import(wordpress_data)
        massage4 = Massage.objects.get(external_id=10)
        self.assertEqual(massage4.status, "approved")
        self.assertEqual(massage4.external_id, 10)

        # massage = Massage.objects.latest("id")
        # massage.refresh_from_db()
        # self.assertEqual(massage.start, expected_date

        # # check wp IDs against local IDs
        wordpress_external_id = massage_appointments(wordpress_data)

        # only_local_db should be [5] only_in_wp_db should be [4]
        only_in_local_db, only_in_wordpress_db = massage_date_comparison_with_wp_db(
            wordpress_external_id
        )
        self.assertEqual(massage.external_id, 15)
        print(only_in_local_db)
        print(only_in_wordpress_db)

        # self.assertEqual((only_in_local_db, only_in_wordpress_db), ([5, 7, 8], [10]))


class LogDataTest(TestCase):
    def test_custom_logger(self):
        customer = CustomerFactory()
        user = UserProfileFactory().user
        user2 = UserProfileFactory().user
        service = ServiceFactory()

        with self.assertLogs("web.importer", level="INFO") as cm:
            massage, created = update_or_create_w_logging(
                Massage,
                external_id=55,
                defaults={
                    "customer": customer,
                    "status": "approved",
                    "service": service,
                    "therapist": user,
                },
            )

            self.assertIn("Imported new", cm.output[0])

        with self.assertLogs("web.importer", level="INFO") as cm:
            massage, created = update_or_create_w_logging(
                Massage,
                external_id=55,
                defaults={
                    "customer": customer,
                    "status": "canceled",
                    "service": service,
                    "therapist": user2,
                },
            )
            self.assertIn("approved => canceled", cm.output[1])


class WordpressApiCallTest(TestCase):
    pass