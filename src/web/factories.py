import factory

from . import models
import pytz

tz = pytz.timezone("Europe/Ljubljana")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    first_name = factory.Sequence(lambda n: "Agent %03d" % n)
    username = factory.Sequence(lambda n: "Agent %03d" % n)
    email = factory.Sequence(lambda n: "Agent %03d" % n)


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.UserProfile

    user = factory.SubFactory(UserFactory)
    external_id = factory.Faker("pyint")


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Customer

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    email = factory.Faker("email")
    phone = factory.Faker("phone_number")
    occupation = factory.Faker("job")
    previous_massage = factory.Faker("pybool")
    salon_choice = factory.Faker("sentence")
    frequency = factory.Faker("sentence")
    referral = factory.Faker("sentence")
    external_id = factory.Faker("pyint")


class MassageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Massage

    customer = factory.SubFactory(CustomerFactory)
    therapist = factory.SubFactory(UserFactory)
    start = factory.Faker("date_time", tzinfo=tz)
    reason_for_visit = factory.Faker("sentence")
    kind = factory.Faker("sentences")
    notes = factory.Faker("sentences")
    next_visit = factory.Faker("sentences")
    recommendations = factory.Faker("sentences")
    personal_notes = factory.Faker("sentences")
    duration = factory.Faker("pyint")
    amount = factory.Faker("pyint")
    discount = factory.Faker("pyint")
    discount_reason = factory.Faker("sentences")
    repeat_visit = factory.Faker("pybool")
    external_id = factory.Faker("pyint")
