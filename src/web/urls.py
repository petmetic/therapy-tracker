from django.urls import path, include
from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("customer_list/", views.customer_list, name="customer_list"),
    path(
        "customer_list/<int:pk>/detail/", views.customer_detail, name="customer_detail"
    ),
    path("customer/<int:customer_pk>/detail/", views.customer, name="customer"),
    path("customer_list/add/", views.customer_add, name="customer_add"),
    path("error/", views.error, name="error"),
    path("massage_list/<int:pk>/detail/", views.massage_detail, name="massage_detail"),
    path("massage_list/<int:customer_pk>/add/", views.massage_add, name="massage_add"),
    path("logout", views.custom_logout, name="logout"),
    path("", views.index, name="index"),
]
