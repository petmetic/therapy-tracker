from django.core.management.base import BaseCommand

from web.models import Customer, User, Massage, Service
from web.wordpress_api_calls import (
    get_therapist_service_data_from_wp,
    get_massage_customer_data_from_wp,
    get_massage_appointments,
    get_single_appointment_data_from_wp,
)
from web.importer import (
    therapist_import,
    services_import,
    customer_import,
    massage_import,
    massage_date_comparison_with_wp_db,
    single_massage_import,
)
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Help to do sync"

    def handle(self, *args, **options):
        # API call for therapists and services
        data_entities = get_therapist_service_data_from_wp()

        # API call for customers and massages
        data_appointments = get_massage_customer_data_from_wp(day_past=1, day_future=7)

        sync_time = datetime.now()
        # import therapist
        logger.info(f"NEW SYNC at {sync_time}")
        therapist_import(data_entities)
        self.stdout.write(self.style.SUCCESS("Successfully synced therapists:"))
        self.stdout.write(str(User.objects.all().count()))
        logger.info(f"Successfully synced therapists at {sync_time}")

        # import services
        services_import(data_entities)
        self.stdout.write(self.style.SUCCESS("Successfully synced services:"))
        self.stdout.write(str(Service.objects.all().count()))
        logger.info(f"Successfully synced services at {sync_time}")

        # import customers
        customer_import(data_appointments)
        self.stdout.write(self.style.SUCCESS("Successfully synced customers:"))
        self.stdout.write(str(Customer.objects.all().count()))
        logger.info(f"Successfully synced customers at {sync_time}")

        # import massages :
        # 1. get appointment IDs from WP
        massage_appointments_in_wp_db = get_massage_appointments(data_appointments)
        self.stdout.write(
            self.style.SUCCESS(
                "Successfully retrieved list of massage_appointments_in_wp_db:"
            )
        )
        self.stdout.write(str(len(massage_appointments_in_wp_db)))
        logger.info(
            f"Successfully retrieved list of massage_appointments_in_wp_db at {sync_time}"
        )

        # 2. check external_id in WP against local_db
        only_in_local_db, only_in_wordpress_db = massage_date_comparison_with_wp_db(
            massage_appointments_in_wp_db
        )
        self.stdout.write(
            self.style.SUCCESS(
                "Successfully successfully checked list of wp_id to local_db:"
            )
        )
        self.stdout.write(self.style.SUCCESS("\tNumber of massages in only local_db:"))
        self.stdout.write(str(len(only_in_local_db)))
        logger.info(f"\tID of massages in only local_db:{only_in_local_db}")
        self.stdout.write(self.style.SUCCESS("\tNumber of massages in only wp_db:"))
        self.stdout.write(str(len(only_in_wordpress_db)))
        logger.info(f"successfully checked list of wp_id to local_db at {sync_time}")

        # 4. import all appointments --> also the ones with changes (canceled ect.)
        massage_import(data_appointments)
        self.stdout.write(
            self.style.SUCCESS("Successfully synced massages from wp_db:")
        )
        self.stdout.write(str(Massage.objects.all().count()))
        logger.info(f"Successfully synced massages from wp_db at {sync_time}")

        # 5. import single_appointments that have only external_id in local_db
        for external_id in only_in_local_db:
            data = get_single_appointment_data_from_wp(external_id=external_id)
            single_massage_import(data)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully checked and synced massages from local_db that are not in wp_db:"
            )
        )
        logger.info(
            f"Successfully checked and synced massages from local_db that are not in wp_db: at {sync_time}"
        )

        self.stdout.write(
            self.style.SUCCESS("Successfully synced massage appointments:")
        )
        self.stdout.write(str(Massage.objects.all().count()))
        logger.info(f"Successfully synced all massage appointments at {sync_time}")
