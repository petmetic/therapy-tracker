import factory

from . import models


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
    external_id = ""


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Customer

    name = factory.Faker("name")
    email = factory.Faker("email")


class MassageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Massage

    date = factory.Faker("date")
    reason_for_visit = factory.Faker("sentence")
    notes = factory.Faker("sentences")
    next_visit = factory.Faker("sentences")
    recommendations = factory.Faker("sentences")
    personal_notes = factory.Faker("sentences")
