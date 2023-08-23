from django.core.management.base import BaseCommand
from ...models import Customer, User, Massage, Service
from ...wordpress_api_calls import (
    get_therapist_service_data_from_wp,
    get_massage_customer_data_from_wp,
    get_wp_credentials,
    get_single_appointment_data_from_wp,
)
from ...importer import (
    therapist_import,
    services_import,
    customer_import,
    # massage_import,
    massage_appointments,
    only_in_wordpress_db_import,
    only_in_local_db_import,
    massage_date_comparison_with_wp_db,
)
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Help to do sync"

    def handle(self, *args, **options):
        nonce, session = get_wp_credentials()
        # API call for therapists and services
        data_entities = get_therapist_service_data_from_wp(nonce=nonce, session=session)
        # API call for customers and massages
        data_appointments = get_massage_customer_data_from_wp(
            day_past=1, day_future=7, nonce=nonce, session=session
        )

        # import services, therapist
        therapist_import(data_entities)
        services_import(data_entities)

        sync_time = datetime.now()
        self.stdout.write(str(Service.objects.all().count()))

        self.stdout.write(self.style.SUCCESS("Successfully synced services"))
        logger.info(f"Successfully synced services at {sync_time}")

        self.stdout.write(str(User.objects.all().count()))
        self.stdout.write(self.style.SUCCESS("Successfully synced therapists"))
        logger.info(f"Successfully synced therapists at {sync_time}")

        # import customers
        customer_import(data_appointments)
        # import appointments
        massage_appointments_in_wp_db = massage_appointments(data_appointments)
        # check against external_id in local_db
        only_in_local_db, only_in_wordpress_db = massage_date_comparison_with_wp_db(
            massage_appointments_in_wp_db
        )
        # import appointments that have no external_id in local_db
        only_in_wordpress_db_import(only_in_wordpress_db, data_appointments)
        #
        for external_id in only_in_local_db:
            data_appointments = get_single_appointment_data_from_wp(
                nonce=nonce, session=session, wp_id=external_id
            )

        """
        massage_import(data_appointments)
        """

        self.stdout.write(str(Customer.objects.all().count()))
        self.stdout.write(self.style.SUCCESS("Successfully synced customers"))
        logger.info(f"Successfully synced customers at {sync_time}")
        self.stdout.write(str(Massage.objects.all().count()))
        self.stdout.write(
            self.style.SUCCESS("Successfully synced massage appointments")
        )
        logger.info(f"Successfully synced massage appointments at {sync_time}")
