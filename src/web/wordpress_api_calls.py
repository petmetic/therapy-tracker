import requests
from datetime import datetime, timedelta

from therapytracker.localsettings import (
    WP_URL_APPOINTMENTS,
    WP_API_KEY,
    WP_URL_ENTITIES,
    WP_URL_SINGLE_APPOINTMENT,
)


def get_massage_customer_data_from_wp(day_past, day_future):
    date_sync_before = (datetime.today() - timedelta(days=day_past)).strftime(
        "%Y-%m-%d"
    )
    date_sync_week = (datetime.today() + timedelta(days=day_future)).strftime(
        "%Y-%m-%d"
    )

    url = requests.get(
        WP_URL_APPOINTMENTS,
        headers={"Amelia": WP_API_KEY},
        data={"date_sync_before": date_sync_before, "date_sync_week": date_sync_week},
    )
    wp_massage_customer = url.json()

    return wp_massage_customer


def get_therapist_service_data_from_wp():
    url = requests.get(WP_URL_ENTITIES, headers={"Amelia": WP_API_KEY})
    wp_therapist_service = url.json()

    return wp_therapist_service


def get_single_appointment_data_from_wp(external_id):
    url = requests.get(
        WP_URL_SINGLE_APPOINTMENT,
        headers={"Amelia": WP_API_KEY, "external_id": external_id},
    )
    wp_single_appointment = url.json()

    return wp_single_appointment


def get_massage_appointments(data: dict) -> list:
    """
    Get a list of external_id from the wodrpess API call
    """
    massages = data["data"]["appointments"]
    wordpress_api_db = []

    for raw_appointment in massages.values():
        individual_appointments = raw_appointment["appointments"]

        for appointment in individual_appointments:
            for app in appointment["bookings"]:
                external_id_massage = app["appointmentId"]  # external_id
                # create a wordpress_db to check against local_db
                wordpress_api_db.append(external_id_massage)

    return wordpress_api_db
