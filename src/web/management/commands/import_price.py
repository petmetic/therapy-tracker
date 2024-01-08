from django.core.management.base import BaseCommand
from web.wordpress_api_calls import (
    get_therapist_service_data_from_wp,
    get_wp_prices,
)
from web.importer import price_import
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import new prices"

    def handle(self, *args, **options):
        # get prices from WP
        data_entities = get_therapist_service_data_from_wp()
        amelia_prices = get_wp_prices(data_entities)

        # import new price in Price table
        sync_time = datetime.now()
        logger.info(f"NEW PRICE SYNC at {sync_time}")
        price_import(amelia_prices)

        logger.info(f"Successfully synced prices at {sync_time}")
