from django.core.management.base import BaseCommand, CommandError
from ...models import Customer
from django.conf import settings
import requests
import requests_cache

session = requests_cache.CachedSession("requests_cache")


class Command(BaseCommand):
    help = "Help to do sync"

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        r = session.get(
            settings.WP_URL_ENTITIES, auth=(settings.WP_USER, settings.WP_PASSWORD)
        )
        print(r.json())
        self.stdout.write(str(Customer.objects.all().count()))
        self.stdout.write(self.style.SUCCESS("Successfully synced"))
