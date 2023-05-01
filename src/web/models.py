from django.db import models
from django.contrib.auth.models import User


class Massage(models.Model):
    customer = models.ForeignKey(
        "Customer",
        on_delete=models.CASCADE,
    )
    therapist = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    massage_date = models.DateTimeField(blank=True, null=True)
    # needs to be date of current massage; can be changed on request by user
    # (not necessarily entered the same date as therapy done)
    reason_for_visit = models.TextField(default="")
    kind = models.CharField(max_length=300)
    massage_notes = models.TextField(default="")
    next_visit = models.TextField(default="", blank=True)
    recommendations = models.TextField(default="", blank=True)
    personal_notes = models.TextField(default="", blank=True)
    duration = models.CharField(max_length=200, default="")
    amount = models.CharField(max_length=200, default="")
    discount = models.CharField(max_length=200, default="", blank=True)
    discount_reason = models.CharField(max_length=200, default="", blank=True)
    repeat_visit = models.BooleanField(default=False)
    status = models.CharField(max_length=200, default="", blank=True)
    service = models.CharField(max_length=200, default="", blank=True)
    external_id = models.CharField(max_length=200, default="", blank=True)

    added = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.massage_date}, {self.customer}"


class Customer(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200, null=True, default="")
    email = models.EmailField(max_length=254, null=True, default="")
    phone = models.CharField(max_length=100, null=True, default="")
    occupation = models.CharField(max_length=200, null=True, default="")
    previous_massage = models.BooleanField(default=False)
    salon_choice = models.CharField(max_length=200, default="")
    frequency = models.CharField(max_length=200, default="")
    referral = models.CharField(max_length=200, default="")
    external_id = models.CharField(blank=True, null=True, default="", max_length=50)

    def __str__(self):
        return f"{self.surname} {self.name}"


class Service(models.Model):
    external_id = models.CharField(blank=True, null=True, default="", max_length=50)
    service_group = models.CharField(max_length=200, null=True, default="")
    price = models.CharField(max_length=200, default="", null=True)
    massage_name = models.CharField(max_length=200, null=True, default="")

    def __str__(self):
        return f"id: {self.external_id}, name: {self.massage_name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    external_id = models.CharField(max_length=200, default="", null=True)
