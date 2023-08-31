import datetime
import pytz
from freezegun import freeze_time

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
    single_massage_import,
    massage_date_comparison_with_wp_db,
)
from ..wordpress_api_calls import get_massage_appointments

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

        customer1 = CustomerFactory.build(name="Brian", main_concern="car accident")
        customer2 = CustomerFactory.build(name="Alice", main_concern="bike accident")
        customer3 = CustomerFactory.build(name="David", main_concern="fall off tree")

        massage1 = MassageFactory.build(
            therapist=therapist1,
            customer=customer1,
            start=datetime.datetime(2023, 4, 6, 16, 0, 0).astimezone(tz=tz),
            status="approved",
            external_id=5,
        )
        massage2 = MassageFactory.build(
            therapist=therapist1,
            customer=customer2,
            start=datetime.datetime(2023, 4, 6, 18, 0, 0).astimezone(tz=tz),
            status="canceled",
            external_id=7,
        )
        massage3 = MassageFactory.build(
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

        massage_appointments_in_wp_db = get_massage_appointments(data)
        self.assertEqual(massage_appointments_in_wp_db, [5, 7, 8])

    @freeze_time("2023-04-06 13:21:34", tz_offset=2)
    def test_massage_date_comparison_with_wp_db(self):
        therapist1 = UserProfileFactory(user__first_name="Jane").user
        self.client.force_login(therapist1)

        customer1 = CustomerFactory(name="Brian")
        customer2 = CustomerFactory(name="Alice")
        customer3 = CustomerFactory(name="David")
        customer4 = CustomerFactory(name="Sam")

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
        massage4 = MassageFactory.build(
            therapist=therapist1,
            customer=customer4,
            start=datetime.datetime(2023, 4, 7, 20, 0, 0).astimezone(tz=tz),
            status="approved",
            external_id=10,
        )

        # does not contain massage4(ex_id=10, name=Sam)
        # contains ex_id=[5, 7, 8]
        massages = list(Massage.objects.values_list("external_id", flat=True))
        self.assertEqual(massages, [5, 7, 8])

        # added massage4(ex_id=10, name=Sam)
        # contains ex_id=[7, 8, 10]
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

        # get WP appointment IDs from WP
        wordpress_external_id = get_massage_appointments(wordpress_data)

        # check against external_id in local_db
        only_in_local_db, only_in_wordpress_db = massage_date_comparison_with_wp_db(
            wordpress_external_id
        )
        self.assertEqual(only_in_local_db, [5])
        self.assertEqual(only_in_wordpress_db, [10])
