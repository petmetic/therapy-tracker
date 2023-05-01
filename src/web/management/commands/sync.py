from django.core.management.base import BaseCommand
from ...models import Customer, User, Massage, Service
import requests_cache
import json
from web.utility import (
    therapist_import,
    services_import,
    customer_import,
    massage_import,
)

session = requests_cache.CachedSession("requests_cache")


class Command(BaseCommand):
    help = "Help to do sync"

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        # r = session.get(
        #     settings.WP_URL_ENTITIES, auth=(settings.WP_USER, settings.WP_PASSWORD)
        # )

        # NOT NEEDED ANYMORE, JUST FOR THE API
        # r2 = session.get(settings.WP_URL_CUSTOMERS, auth=(settings.WP_USER, settings.WP_PASSWORD))
        # with open("/Users/meta/code/hacking/therapy-tracker/users_PP_alenka.json") as f:
        #     data = json.loads(f.read())
        #     customers = data['data']['users']
        #
        #
        with open(
            "/Users/meta/code/hacking/therapy-tracker/therapists_PP_alenka.json"
        ) as f:
            data = json.loads(f.read())
            therapists = data["data"]["employees"]
            services = data["data"]["categories"]

            for raw_therapist in therapists:
                therapist_import(raw_therapist)

            for raw_service in services:
                services_import(raw_service)

        self.stdout.write(str(Service.objects.all().count()))
        self.stdout.write(self.style.SUCCESS("Successfully synced services"))

        self.stdout.write(str(User.objects.all().count()))
        self.stdout.write(self.style.SUCCESS("Successfully synced therapists"))

        with open(
            "/Users/meta/code/hacking/therapy-tracker/appointments_PP_alenka.json"
        ) as f:
            data = json.loads(f.read())
            massages = data["data"]["appointments"]

            for raw_appointment in massages.values():
                customer_import(raw_appointment)
                massage_import(raw_appointment)

        self.stdout.write(str(Customer.objects.all().count()))
        self.stdout.write(self.style.SUCCESS("Successfully synced customers"))
        self.stdout.write(str(Massage.objects.all().count()))
        self.stdout.write(
            self.style.SUCCESS("Successfully synced massage appointments")
        )
