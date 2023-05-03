from django.contrib import admin
from .models import Customer, Massage, Service, UserProfile

admin.site.register(Customer)
admin.site.register(Massage)
admin.site.register(Service)
admin.site.register(UserProfile)
