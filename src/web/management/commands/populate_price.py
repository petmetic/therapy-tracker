from datetime import datetime

from django.core.management.base import BaseCommand
from web.models import Price, Service
import logging
import pytz

logger = logging.getLogger(__name__)
tz = pytz.timezone("Europe/Ljubljana")


class Command(BaseCommand):
    help = "Help to populate price model with new prices"

    def handle(self, *args, **options):
        for service in Service.objects.all():
            service_price = service.price
            payout = service.payout
            start_date = datetime(2023, 1, 1, 0, 00, 00).astimezone(tz=tz)
            # maybe add just prices that are new? do not have duplicates inside?
            Price.objects.create(
                service=service,
                cost=service_price,
                payout=payout,
                start_date=start_date,
                end_date=None,
            )

        sync_time = datetime.now()
        logger.info(f"Successfully populated prices at {sync_time}")
