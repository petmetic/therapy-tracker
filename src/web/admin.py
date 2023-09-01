from django.contrib import admin
from .models import Customer, Massage, Service, UserProfile, Billable

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
    ]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_filter = ["name", "price"]


@admin.register(Billable)
class BillableAdmin(admin.ModelAdmin):
    list_filter = ["therapist", "service"]
