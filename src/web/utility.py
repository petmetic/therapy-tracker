from .models import User, UserProfile, Service, Massage, Customer


def therapist_import(data):
    therapists = data["data"]["employees"]

    for raw_therapist in therapists:
        user, created = User.objects.get_or_create(
            first_name=raw_therapist.get("firstName"),
            email=raw_therapist.get("email"),
            username=raw_therapist.get("email"),
        )

        UserProfile.objects.get_or_create(
            user=user,
            external_id=raw_therapist.get("id"),
        )

    return user


def services_import(data):
    services = data["data"]["categories"]
    for raw_service in services:
        service_group = raw_service["name"]
        for individual_service in raw_service["serviceList"]:
            service_list_id = individual_service["id"]
            service_list_name = individual_service["name"]
            price = individual_service["price"]

            service = Service.objects.get_or_create(
                service_group=service_group,
                external_id=service_list_id,
                name=service_list_name,
                price=price,
            )

    return service


def customer_import(data):
    massages = data["data"]["appointments"]

    for raw_appointment in massages.values():
        individual_appointments = raw_appointment["appointments"]
        for appointment in individual_appointments:
            for app in appointment["bookings"]:
                external_id_customer = app["customer"]["id"]
                name_customer = app["customer"]["firstName"]
                surname_customer = app["customer"]["lastName"]
                email_customer = app["customer"]["email"]
                phone_customer = app["customer"]["phone"]

                customer, created = Customer.objects.get_or_create(
                    external_id=external_id_customer,
                    defaults={
                        "name": name_customer,
                        "surname": surname_customer,
                        "email": email_customer,
                        "phone": phone_customer,
                    },
                )
    return customer


def massage_import(data):
    massages = data["data"]["appointments"]
    for raw_appointment in massages.values():
        massage_date = raw_appointment["date"]
        #  TODO: import bookingStart and pars the string to datetime object
        individual_appointments = raw_appointment["appointments"]

        for appointment in individual_appointments:
            service = appointment["serviceId"]
            therapist = User.objects.filter(
                userprofile__external_id=appointment["providerId"]
            ).first()
            status = appointment["status"]
            for app in appointment["bookings"]:
                external_id_massage = app["id"]
                external_id_customer = app["customer"]["id"]
                customer, created = Customer.objects.get_or_create(
                    external_id=external_id_customer,
                )

                service_massage, created = Service.objects.get_or_create(
                    name=service,
                )

                massage = Massage.objects.get_or_create(
                    massage_date=massage_date,
                    customer=customer,
                    status=status,
                    service=service_massage,
                    external_id=external_id_massage,
                    therapist=therapist,
                )

    return massage
