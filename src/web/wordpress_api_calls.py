import requests
import re
import json
from django.conf import settings
from datetime import datetime, timedelta


def get_wp_credentials():
    regex = r"var\s+wpAmeliaNonce\s*=\s*['\"]?([a-fA-F0-9]+)['\"]?"

    session = requests.Session()
    headers1 = {"Cookie": "wordpress_test_cookie=WP Cookie check"}
    datas = {
        "log": settings.WP_USER,
        "pwd": settings.WP_PASSWORD,
        "wp-submit": "Log In",
        "redirect_to": settings.WP_ADMIN,
        "testcookie": "1",
    }
    session.post(settings.WP_LOGIN, headers=headers1, data=datas)
    resp = session.get(settings.WP_ADMIN)

    match = re.search(regex, resp.text)
    if not match:
        print("No nonce found")
        return
    nonce = match.group(1)

    return nonce, session


def get_massage_customer_data_from_wp(day_past, day_future, nonce, session):
    date_sync_before = (datetime.today() - timedelta(days=day_past)).strftime(
        "%Y-%m-%d"
    )
    date_sync_week = (datetime.today() + timedelta(days=day_future)).strftime(
        "%Y-%m-%d"
    )

    url = settings.WP_URL_APPOINTMENTS.format(
        nonce=nonce,
        date_sync_before=date_sync_before,
        date_sync_week=date_sync_week,
    )
    wp_json = session.get(url).text
    wp_massage_customer = json.loads(wp_json)

    return wp_massage_customer


def get_therapist_service_data_from_wp(nonce, session):
    url = settings.WP_URL_ENTITIES.format(nonce=nonce)
    wp_json = session.get(url).text
    wp_therapist_service = json.loads(wp_json)

    return wp_therapist_service


def get_single_appointment_data_from_wp(nonce, session, external_id):
    url = settings.WP_URL_SINGLE_APPOINTMENT.format(
        nonce=nonce, external_id=external_id
    )
    wp_json = session.get(url).text
    wp_single_appointment = json.loads(wp_json)

    return wp_single_appointment
