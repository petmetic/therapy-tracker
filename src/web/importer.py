from web.models import User, UserProfile, Service, Massage, Customer, Price
from datetime import datetime, timedelta
import pytz
import dictdiffer
import logging

logger = logging.getLogger(__name__)

tz = pytz.timezone("Europe/Ljubljana")


def update_or_create_w_logging(model, external_id, defaults):
    sync_time = datetime.now()
    model_name = model.__name__
    old_dict = {}
    new_dict = {}
    try:
        old_model = model.objects.get(external_id=external_id)
    except model.DoesNotExist:
        old_model = None

    if old_model:
        for key in defaults.keys():
            old_dict[key] = getattr(old_model, key)

    new_model, created = model.objects.update_or_create(
        external_id=external_id, defaults=defaults
    )

    for key in defaults.keys():
        new_dict[key] = getattr(new_model, key)

    difference = list(dictdiffer.diff(old_dict, new_dict))

    if created:
        logger.info(f"Imported new {model_name} with {new_model.external_id}")
    elif difference:
        logger.info(f"Changes were found when syncing {model_name} at {sync_time}:")
        for kind, field, change in difference:
            logger.info(
                f"name: {old_model}, external id:{old_model.external_id}\n{kind}:\n\t{field}: {change[0]} => {change[1]}\n"
            )

    return model, created


def therapist_import(data: dict):
    therapists = data["data"]["employees"]

    for raw_therapist in therapists:
        external_id = raw_therapist.get("id")
        first_name = raw_therapist.get("firstName")
        email = raw_therapist.get("email")
        username = raw_therapist.get("email")

        # check if external_id exists
        if User.objects.filter(userprofile__external_id=external_id):
            user_profile = UserProfile.objects.get(external_id=external_id)
            changed = False
            user = user_profile.user

            if email != user.email:
                logger.info(
                    f"Changed therapist {user} with external_id: {user_profile.external_id}\n"
                    f"\t email - from {user.email} to {email}\n"
                    f"\t username - from {user.username} to {username}"
                )
                user.email = email
                # email and username are the same
                user.username = username
                changed = True

            if first_name != user.first_name:
                logger.info(
                    f"Changed therapist {user} with external_id: {user_profile.external_id}\n"
                    f"\t first_name - from {user.first_name} to {first_name}"
                )
                user.first_name = first_name
                changed = True

            if changed:
                user.save()

        else:
            # if not, create it
            user = User.objects.create(
                first_name=first_name,
                email=email,
                username=username,
            )

            UserProfile.objects.create(
                user=user,
                external_id=external_id,
            )
            logger.info(f"Imported new therapist with external_id: {external_id}")

    return user


def services_import(data: dict):
    services = data["data"]["categories"]
    for raw_service in services:
        service_group = raw_service["name"]
        for individual_service in raw_service["serviceList"]:
            service_list_id = individual_service["id"]
            service_list_name = individual_service["name"]
            price = individual_service["price"]
            duration = individual_service["duration"]
            time_before = individual_service["timeBefore"]
            if time_before is None:
                time_before = 0

            time_after = individual_service["timeAfter"]
            if time_after is None:
                time_after = 0

            service, created = update_or_create_w_logging(
                Service,
                external_id=service_list_id,
                defaults={
                    "service_group": service_group,
                    "name": service_list_name,
                    "price": price,
                    "duration": duration,
                    "time_before": time_before,
                    "time_after": time_after,
                },
            )

    return service


def customer_import(data: dict):
    massages = data["data"]["appointments"]

    for raw_massage in massages.values():
        individual_massage = raw_massage["appointments"]
        for massage in individual_massage:
            for field in massage["bookings"]:
                external_id_customer = field["customer"]["id"]
                name_customer = field["customer"]["firstName"]
                surname_customer = field["customer"]["lastName"]
                email_customer = field["customer"]["email"]
                phone_customer = field["customer"]["phone"]

                customer, created = update_or_create_w_logging(
                    Customer,
                    external_id=external_id_customer,
                    defaults={
                        "name": name_customer,
                        "surname": surname_customer,
                        "email": email_customer,
                        "phone": phone_customer,
                    },
                )
    return customer


def massage_import(data: dict):
    massages = data["data"]["appointments"]
    tz = pytz.timezone("Europe/Ljubljana")

    for raw_appointment in massages.values():
        individual_appointments = raw_appointment["appointments"]

        for appointment in individual_appointments:
            service = appointment["serviceId"]
            massage_start = datetime.strptime(
                appointment["bookingStart"], "%Y-%m-%d %H:%M:%S"
            ).astimezone(tz=tz)
            massage_end = datetime.strptime(
                appointment["bookingEnd"], "%Y-%m-%d %H:%M:%S"
            ).astimezone(tz=tz)
            therapist = User.objects.filter(
                userprofile__external_id=appointment["providerId"]
            ).first()
            status = appointment["status"]
            for app in appointment["bookings"]:
                external_id_massage = app["appointmentId"]
                external_id_customer = app["customer"]["id"]
                customer = Customer.objects.get(
                    external_id=external_id_customer,
                )
                service_massage = Service.objects.get(
                    external_id=service,
                )

                massage, created = update_or_create_w_logging(
                    Massage,
                    external_id=external_id_massage,
                    defaults={
                        "customer": customer,
                        "status": status,
                        "service": service_massage,
                        "therapist": therapist,
                        "start": massage_start,
                        "end": massage_end,
                    },
                )

    return massage


def single_massage_import(data: dict):
    massages = data["data"]["appointment"]
    tz = pytz.timezone("Europe/Ljubljana")

    external_id_massage = massages["id"]
    service = massages["serviceId"]
    service_massage = Service.objects.get(
        external_id=service,
    )
    massage_start = datetime.strptime(
        massages["bookingStart"], "%Y-%m-%d %H:%M:%S"
    ).astimezone(tz=tz)
    massage_end = datetime.strptime(
        massages["bookingEnd"], "%Y-%m-%d %H:%M:%S"
    ).astimezone(tz=tz)
    therapist = User.objects.filter(
        userprofile__external_id=massages["providerId"]
    ).first()
    status = massages["status"]

    for app in massages["bookings"]:
        external_id_customer = app["customerId"]
        customer = Customer.objects.get(
            external_id=external_id_customer,
        )

    massage, created = update_or_create_w_logging(
        Massage,
        external_id=external_id_massage,
        defaults={
            "customer": customer,
            "status": status,
            "service": service_massage,
            "therapist": therapist,
            "start": massage_start,
            "end": massage_end,
        },
    )
    return massage


def massage_date_comparison_with_wp_db(wordpress_api_db: list) -> tuple[[list], [list]]:
    """
    Checking the db of massages for a day in past and week in future against the wordpress_api_ db from the Wordpress API.
    """

    tz = pytz.timezone("Europe/Ljubljana")
    # because start__range=(date_sync_before, date_sync_week) is a given as range,
    # it is checked for 7 days in future + 1 day
    date_sync_before = (datetime.today() - timedelta(days=1)).astimezone(tz=tz)
    date_sync_week = (datetime.today() + timedelta(days=8)).astimezone(tz=tz)

    local_db = set(
        Massage.objects.filter(
            start__range=(date_sync_before, date_sync_week)
        ).values_list("external_id", flat=True)
    )
    wordpress_api_db = set(wordpress_api_db)

    only_in_local_db = sorted(local_db.difference(wordpress_api_db))
    only_in_wordpress_db = sorted(wordpress_api_db.difference(local_db))

    return only_in_local_db, only_in_wordpress_db


def price_import(data: list):
    start_date = datetime.now().astimezone(tz=tz)
    end_date = datetime.now().astimezone(tz=tz)

    # get Services from the db
    for service in Service.objects.all():
        service_external_id = service.external_id
        for amelia_service_id, amelia_service_price in data:
            # check the latest price of service (end_date=None)
            if service_external_id == amelia_service_id:
                current_price = Price.objects.get(service=service, end_date=None)
                # compare WP prices with latest service price
                if current_price.cost != amelia_service_price:
                    logger.info(
                        f"Imported new service: {service}"
                        f"\n\tPrice change from {current_price.cost} eur to {amelia_service_price} eur."
                    )
                    current_price.end_date = end_date
                    current_price.save()
                    # if price different -> New db entry
                    Price.objects.create(
                        service=service,
                        cost=amelia_service_price,
                        payout=current_price.payout,
                        start_date=start_date,
                        end_date=None,
                    )
