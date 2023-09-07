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

from ..importer import (
    customer_import,
    massage_import,
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
