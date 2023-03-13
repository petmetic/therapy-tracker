from django.db import models
from django.contrib.auth.models import User


class Massage(models.Model):
    client = models.ForeignKey('Customer', on_delete=models.CASCADE, )
    customer = models.ForeignKey('Profile', on_delete=models.CASCADE, )
    massage_date = models.DateTimeField(blank=True,
                                        null=True)  # needs to be date of current massage; can be changed n request by user (not neccessarily entered the same date as therapy done)
    reason_for_visit = models.TextField(default='')
    kind = models.CharField(max_length=300)
    massage_notes = models.TextField(default='')
    instruction_notes = models.TextField(default='')
    personal_notes = models.TextField(default='')
    duration = models.IntegerField(default='')
    amount = models.IntegerField()
    discount = models.TextField(default='')
    repeat_visit = models.BooleanField(default=False)

    added = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)


class Customer(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=100)
    occupation = models.CharField(max_length=200)
    previous_massage = models.TextField(default='')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # delete when user is deleted

    def __str__(self):
        return f'{self.user.username} Profile'  # show how we want it to display
