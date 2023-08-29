import pytz

from django.test import TestCase

from .factories import (
    CustomerFactory,
    UserProfileFactory,
    ServiceFactory,
)
from ..models import Massage
from ..importer import (
    update_or_create_w_logging,
)

tz = pytz.timezone("Europe/Ljubljana")


class LogDataTest(TestCase):
    def test_custom_logger(self):
        customer = CustomerFactory()
        user = UserProfileFactory().user
        user2 = UserProfileFactory().user
        service = ServiceFactory()

        with self.assertLogs("web.importer", level="INFO") as cm:
            massage, created = update_or_create_w_logging(
                Massage,
                external_id=55,
                defaults={
                    "customer": customer,
                    "status": "approved",
                    "service": service,
                    "therapist": user,
                },
            )

            self.assertIn("Imported new", cm.output[0])

        with self.assertLogs("web.importer", level="INFO") as cm:
            massage, created = update_or_create_w_logging(
                Massage,
                external_id=55,
                defaults={
                    "customer": customer,
                    "status": "canceled",
                    "service": service,
                    "therapist": user2,
                },
            )
            self.assertIn("approved => canceled", cm.output[1])


class WordpressApiCallTest(TestCase):
    pass
