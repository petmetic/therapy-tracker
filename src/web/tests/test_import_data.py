import datetime
import pytz

from django.test import TestCase

from .factories import (
    CustomerFactory,
    MassageFactory,
    UserProfileFactory,
    ServiceFactory,
)
from ..models import Massage, Customer, User, Service
from ..importer import (
    therapist_import,
    services_import,
    customer_import,
    massage_import,
)

tz = pytz.timezone("Europe/Ljubljana")


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
