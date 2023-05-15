from django.core.management.base import BaseCommand
from ...models import Customer, User, Massage, Service
import requests
import re
from django.conf import settings
import json
from ...utility import (
    therapist_import,
    services_import,
    customer_import,
    massage_import,
)


class Command(BaseCommand):
    help = "Help to do sync"

    def handle(self, *args, **options):
        regex = r"var\s+wpAmeliaNonce\s*=\s*['\"]?([a-fA-F0-9]+)['\"]?"

        with requests.Session() as s:
            headers1 = {"Cookie": "wordpress_test_cookie=WP Cookie check"}
            datas = {
                "log": settings.WP_USER,
                "pwd": settings.WP_PASSWORD,
                "wp-submit": "Log In",
                "redirect_to": settings.WP_ADMIN,
                "testcookie": "1",
            }
            s.post(settings.WP_LOGIN, headers=headers1, data=datas)
            resp = s.get(settings.WP_ADMIN)

            match = re.search(regex, resp.text)
            if not match:
                print("No nonce found")
                return
            nonce = match.group(1)
            entities_json = s.get(settings.WP_URL_ENTITIES.format(nonce)).text
            data_entities = json.loads(entities_json)

            appointments_json = s.get(settings.WP_URL_APPOINTMENTS.format(nonce)).text
            data_appointments = json.loads(appointments_json)

        # import services, therapists
        therapist_import(data_entities)
        services_import(data_entities)

        self.stdout.write(str(Service.objects.all().count()))
        self.stdout.write(self.style.SUCCESS("Successfully synced services"))

        self.stdout.write(str(User.objects.all().count()))
        self.stdout.write(self.style.SUCCESS("Successfully synced therapists"))

        # import appointments
        customer_import(data_appointments)
        massage_import(data_appointments)

        self.stdout.write(str(Customer.objects.all().count()))
        self.stdout.write(self.style.SUCCESS("Successfully synced customers"))
        self.stdout.write(str(Massage.objects.all().count()))
        self.stdout.write(
            self.style.SUCCESS("Successfully synced massage appointments")
        )
