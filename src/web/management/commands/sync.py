from django.core.management.base import BaseCommand, CommandError
from ...models import Customer, User, Massage, Service
from django.conf import settings
import requests_cache
import json
from icecream import ic

session = requests_cache.CachedSession("requests_cache")


class Command(BaseCommand):
    help = "Help to do sync"

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        r = session.get(
            settings.WP_URL_ENTITIES, auth=(settings.WP_USER, settings.WP_PASSWORD)
        )

        # NOT NEEDED ANYMORE, JUST FOR THE API
        # r2 = session.get(settings.WP_URL_CUSTOMERS, auth=(settings.WP_USER, settings.WP_PASSWORD))
        # with open("/Users/meta/code/hacking/therapy-tracker/users_PP_alenka.json") as f:
        #     data = json.loads(f.read())
        #     customers = data['data']['users']
        #
        #
        # with open("/Users/meta/code/hacking/therapy-tracker/therapists_PP_alenka.json") as f:
        #     data = json.loads(f.read())
        #     therapists = data['data']['employees']
        #     services = data['data']['categories']
        #
        #     for raw_therapist in therapists:
        #         User.objects.get_or_create(
        #             external_id=raw_therapist.get('id'),
        #             first_name=raw_therapist.get('firstName'),
        #             email=raw_therapist.get('email'),
        #             username=raw_therapist.get('email'),
        #         )
        #
        #     for raw_service in services:
        #         service_group = raw_service['name']
        #         for individual_service in raw_service['serviceList']:
        #             service_list_id = individual_service['id']
        #             service_list_name = individual_service['name']
        #             price = individual_service['price']
        #
        # Service.objects.get_or_create(
        #     service_group=service_group,
        #     external_id=service_list_id,
        #     massage_name=service_list_name,
        #     price=price,
        # )
        #
        # self.stdout.write(str(Service.objects.all().count()))
        # self.stdout.write(self.style.SUCCESS("Successfully synced appointments"))
        #
        # self.stdout.write(str(User.objects.all().count()))
        # self.stdout.write(self.style.SUCCESS("Successfully synced therapists"))

        with open(
            "/Users/meta/code/hacking/therapy-tracker/appointments_PP_alenka.json"
        ) as f:
            data = json.loads(f.read())
            massages = data["data"]["appointments"]

            for raw_appointment in massages.values():
                massage_date = raw_appointment["date"]
                individual_appointments = raw_appointment["appointments"]
                for appointment in individual_appointments:
                    service = appointment["serviceId"]
                    therapist = appointment["providerId"]
                    # TODO: use `therapist` as lookup key for User's external key
                    status = appointment["status"]
                    for app in appointment["bookings"]:
                        external_id_massage = app["id"]
                        external_id_customer = app["customer"]["id"]
                        name_customer = app["customer"]["firstName"]
                        surname_customer = app["customer"]["lastName"]
                        email_customer = app["customer"]["email"]
                        phone_customer = app["customer"]["phone"]

                        customer, created = Customer.objects.get_or_create(
                            external_id=external_id_customer,
                            name=name_customer,
                            surname=surname_customer,
                            email=email_customer,
                            phone=phone_customer,
                        )  # TODO: use `customer` as lookup key for Customer's external key

                        Massage.get_or_create(
                            massage_date=massage_date,
                            customer=customer,
                            status=status,
                            service=service,
                            external_id=external_id_massage,
                            therapist=None,  # User from database
                        )
        self.stdout.write(str(Customer.objects.all().count()))
        self.stdout.write(self.style.SUCCESS("Successfully synced customers"))
        self.stdout.write(str(Massage.objects.all().count()))
        self.stdout.write(
            self.style.SUCCESS("Successfully synced massage appointments")
        )
