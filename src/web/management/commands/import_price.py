from datetime import datetime

from django.core.management.base import BaseCommand
from web.models import Price, Service


class Command(BaseCommand):
    help = "Help to populate price model with new prices"

    def handle(self, *args, **options):
        pass
