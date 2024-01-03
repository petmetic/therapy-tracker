import requests
from datetime import datetime, timedelta

from django.conf import settings


def get_massage_customer_data_from_wp(day_past, day_future):
    date_sync_before = (datetime.today() - timedelta(days=day_past)).strftime(
        "%Y-%m-%d"
    )
    date_sync_week = (datetime.today() + timedelta(days=day_future)).strftime(
        "%Y-%m-%d"
    )

    response = requests.get(
        settings.WP_URL_APPOINTMENTS.format(
            date_sync_before=date_sync_before,
            date_sync_week=date_sync_week,
        ),
        headers={"Amelia": settings.WP_API_KEY},
    )

    wp_massage_customer = response.json()

    return wp_massage_customer


def get_therapist_service_data_from_wp():
    response = requests.get(
        settings.WP_URL_ENTITIES, headers={"Amelia": settings.WP_API_KEY}
    )
    wp_therapist_service = response.json()

    return wp_therapist_service


def get_single_appointment_data_from_wp(external_id):
    response = requests.get(
        settings.WP_URL_SINGLE_APPOINTMENT.format(external_id=external_id),
        headers={"Amelia": settings.WP_API_KEY},
    )
    wp_single_appointment = response.json()

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
