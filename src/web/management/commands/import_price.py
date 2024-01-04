from datetime import datetime

from django.core.management.base import BaseCommand
from web.models import Price
from web.wordpress_api_calls import (
    get_therapist_service_data_from_wp,
    get_massage_customer_data_from_wp,
)
from web.importer import price_parser, price_start_date_parser

from icecream import ic


class Command(BaseCommand):
    help = "Import new prices"

    def handle(self, *args, **options):
        data_entities = get_therapist_service_data_from_wp()
        prices = price_parser(data_entities)
        ic(prices)

        data_appointments = get_massage_customer_data_from_wp(day_past=1, day_future=7)
        start_dates = price_start_date_parser(data_appointments)
        ic(start_dates)
        breakpoint()

        start_date = datetime(2023, 1, 1)
        end_date = None
        Price.objects.create(
            service=service,
            cost=service_price,
            payout=payout,
            start_date=start_date,
            end_date=end_date,
        )
