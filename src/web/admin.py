from django.contrib import admin
from .models import Customer, Massage, Service, UserProfile, Price

admin.site.register(UserProfile)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_filter = ["frequency"]


@admin.register(Massage)
class MassageAdmin(admin.ModelAdmin):
    list_filter = [
        "customer",
        "therapist",
        "kind",
        "duration",
        "amount",
        "discount",
        "status",
        "service",
        "start",
        "external_id",
        "added",
        "changed",
    ]
    list_display = ["external_id", "customer", "therapist", "start"]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_filter = ["name", "price"]
    list_display = ["service_group", "name", "price"]


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_filter = ["service", "start_date", "end_date", "cost", "payout"]
    list_display = ["service", "start_date", "end_date", "cost", "payout"]
