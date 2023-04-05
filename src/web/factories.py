import factory.fuzzy

from . import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Sequence(lambda n: "Agent %03d" % n)


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Customer

    name = factory.Faker("name")
    email = factory.Faker("email")


class MassageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Massage

    massage_date = factory.Faker("date")
    reason_for_visit = factory.Faker("sentence")
    massage_notes = factory.Faker("sentences")
    next_visit = factory.Faker("sentences")
    recommendations = factory.Faker("sentences")
    personal_notes = factory.Faker("sentences")
