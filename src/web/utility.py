from .models import User, UserProfile, Service, Massage, Customer
from datetime import datetime
import pytz
import dictdiffer
import logging

logger = logging.getLogger(__name__)


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
        # logger.info(
        #     f"These changes were made to old model with external id: {old_model.external_id}\n: {difference}\n"
        # )
    # else:
    #     logger.info(f"No changes were made when syncing {model_name}.\n")

    # logger.info(f"Successfully synced {model_name} at {sync_time}.")

    return model, created


def therapist_import(data: dict):
    therapists = data["data"]["employees"]

    for raw_therapist in therapists:
        external_id = raw_therapist.get("id")
        first_name = raw_therapist.get("firstName")
        email = raw_therapist.get("email")
        username = raw_therapist.get("email")

        # check if external_id exists
        if User.objects.get(userprofile__external_id=external_id):
            user, created = update_or_create_w_logging(
                User,
                first_name=first_name,
                email=email,
                username=username,
            )

            userprofile, created = update_or_create_w_logging(
                UserProfile,
                external_id=external_id,
                defaults={
                    "user": user,
                },
            )
        else:
            # if not, create it
            user, created = User.objects.create(
                first_name=first_name,
                email=email,
                username=username,
            )

            UserProfile.objects.create(
                user=user,
                external_id=external_id,
            )

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
