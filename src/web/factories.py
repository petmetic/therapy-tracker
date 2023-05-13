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

    name = factory.Faker("name")
    email = factory.Faker("email")


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
