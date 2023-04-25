from django.core.management.base import BaseCommand, CommandError
from ...models import Customer, User, Massage
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

        # r2 = session.get(settings.WP_URL_CUSTOMERS, auth=(settings.WP_USER, settings.WP_PASSWORD))
        # with open("/Users/meta/code/hacking/therapy-tracker/users_PP_alenka.json") as f:
        #     data = json.loads(f.read())
        #     customers = data['data']['users']
        #
        #     for raw_customer in customers:
        #         Customer.objects.create(
        #             external_id=raw_customer.get('id'),
        #             name=raw_customer.get('firstName'),
        #             surname=raw_customer.get('lastName'),
        #             email=raw_customer.get('email'),
        #             phone=raw_customer.get('phone')
        #         )
        #
        # self.stdout.write(str(Customer.objects.all().count()))
        # self.stdout.write(self.style.SUCCESS("Successfully synced customers"))
        #
        # with open("/Users/meta/code/hacking/therapy-tracker/therapists_PP_alenka.json") as f:
        #     data = json.loads(f.read())
        #     therapists = data['data']['employees']
        #
        #     for raw_therapist in therapists:
        #         User.objects.get_or_create(
        #             # external_id=raw_therapist.get('id'),
        #             first_name=raw_therapist.get('firstName'),
        #             email=raw_therapist.get('email'),
        #             username=raw_therapist.get('email'),
        #         )
        # self.stdout.write(str(User.objects.all().count()))
        # self.stdout.write(self.style.SUCCESS("Successfully synced therapists"))

        with open(
            "/Users/meta/code/hacking/therapy-tracker/appointments_PP_alenka.json"
        ) as f:
            data = json.loads(f.read())
            massages = data["data"]["appointments"]

            for dates, appointments in massages.items():
                for app in appointments["appointments"]:
                    customer, created = Customer.objects.get_or_create(
                        external_id=app["bookings"][0]["customer"].get("id"),
                        name=app["bookings"][0]["customer"].get("firstName"),
                        surname=app["bookings"][0]["customer"].get("lastName"),
                        email=app["bookings"][0]["customer"].get("email"),
                        phone=app["bookings"][0]["customer"].get("phone"),
                    )
                    therapist = User.objects.get()

                    Massage.objects.get_or_create(
                        massage_date=app.get("bookingStart"),
                        customer=customer,
                        status=app.get("status"),
                        service=app.get("serviceId"),
                        therapist_id=app.get("providerId"),
                    )
