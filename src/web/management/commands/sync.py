from django.core.management.base import BaseCommand, CommandError
from ...models import Customer
from django.conf import settings
import requests
import requests_cache
import json

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
        with open("/Users/meta/code/hacking/therapy-tracker/users_PP_alenka.json") as f:
            data = json.loads(f.read())

        print(data)

        self.stdout.write(str(Customer.objects.all().count()))
        self.stdout.write(self.style.SUCCESS("Successfully synced"))
