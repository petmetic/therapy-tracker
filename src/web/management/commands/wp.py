import json

import requests
from django.core.management.base import BaseCommand
import re
from django.conf import settings


class Command(BaseCommand):
    help = "Help to do sync"

    def handle(self, *args, **options):
        wp_login = settings.WP_LOGIN
        wp_admin = settings.WP_ADMIN
        username = settings.WP_USER
        password = settings.WP_PASSWORD

        regex = r"var\s+wpAmeliaNonce\s*=\s*['\"]?([a-fA-F0-9]+)['\"]?"

        with requests.Session() as s:
            headers1 = {"Cookie": "wordpress_test_cookie=WP Cookie check"}
            datas = {
                "log": username,
                "pwd": password,
                "wp-submit": "Log In",
                "redirect_to": wp_admin,
                "testcookie": "1",
            }
            s.post(wp_login, headers=headers1, data=datas)
            resp = s.get(wp_admin)

            match = re.search(regex, resp.text)
            if not match:
                print(f"No nonce found")
                return

            nonce = match.group(1)
            entities_json = s.get(settings.WP_URL_ENTITIES.format(nonce)).text
            data_entities = json.loads(entities_json)

            appointments_json = s.get(settings.WP_URL_APPOINTMENTS.format(nonce)).text
            data_appointments = json.loads(appointments_json)
