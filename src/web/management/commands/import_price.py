from django.core.management.base import BaseCommand
from web.wordpress_api_calls import (
    get_therapist_service_data_from_wp,
    get_wp_prices,
)
from web.importer import price_import


class Command(BaseCommand):
    help = "Import new prices"

    def handle(self, *args, **options):
        # get prices from WP
        data_entities = get_therapist_service_data_from_wp()
        amelia_prices = get_wp_prices(data_entities)
        # import new price in Price table
        price_import(amelia_prices)
