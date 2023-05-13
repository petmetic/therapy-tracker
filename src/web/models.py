from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Massage(models.Model):
    customer = models.ForeignKey(
        "Customer",
        on_delete=models.CASCADE,
    )
    therapist = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    reason_for_visit = models.TextField(default="")
    kind = models.CharField(max_length=300)
    notes = models.TextField(default="")
    next_visit = models.TextField(default="", blank=True)
    recommendations = models.TextField(default="", blank=True)
    personal_notes = models.TextField(default="", blank=True)
    duration = models.IntegerField(default=0, null=True)
    amount = models.IntegerField(default=0, null=True)
    discount = models.IntegerField(default=0, blank=True, null=True)
    discount_reason = models.CharField(max_length=200, default="", blank=True)
    repeat_visit = models.BooleanField(default=False)
    status = models.CharField(max_length=200, default="", blank=True)
    service = models.ForeignKey(
        "Service", on_delete=models.CASCADE, default="", null=True
    )
    external_id = models.IntegerField(default=0, blank=True, null=True)

    added = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.date}, {self.customer}"


class Customer(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200, null=True, default="")
    email = models.EmailField(max_length=254, null=True, default="")
    phone = models.CharField(max_length=100, null=True, default="")
    occupation = models.CharField(max_length=200, null=True, default="", blank=True)
    previous_massage = models.BooleanField(default=False)
    salon_choice = models.CharField(max_length=200, default="", blank=True)
    frequency = models.CharField(max_length=200, default="", blank=True)
    referral = models.CharField(max_length=200, default="", blank=True)
    external_id = models.CharField(blank=True, null=True, default="", max_length=50)

    def __str__(self):
        return f"{self.surname} {self.name}"


class Service(models.Model):
    external_id = models.IntegerField(blank=True, null=True, default=0)
    service_group = models.CharField(max_length=200, null=True, default="")
    name = models.CharField(max_length=200, null=True, default="")
    price = models.IntegerField(default=0, null=True)
    duration = models.IntegerField(default=0)
    time_before = models.IntegerField(default=0)
    time_after = models.IntegerField(default=0)

    def __str__(self):
        return f"external_id: {self.external_id}, service group: {self.service_group}, name: {self.name}"


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    external_id = models.CharField(max_length=200, default="", null=True)
