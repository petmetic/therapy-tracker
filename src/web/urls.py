from django.urls import path, include
from . import views

urlpatterns = [
    path("accounts/login/", views.CustomLoginView.as_view(), name="login"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("customer_list/", views.customer_list, name="customer_list"),
    path(
        "customer_list/<int:pk>/detail/", views.customer_detail, name="customer_detail"
    ),
    path("customer/<int:customer_pk>/detail/", views.customer, name="customer"),
    path("customer/<int:customer_pk>/edit/", views.customer_edit, name="customer_edit"),
    path("customer_list/add/", views.customer_add, name="customer_add"),
    path("error/", views.error, name="error"),
    path("massage_list/<int:pk>/detail/", views.massage_detail, name="massage_detail"),
    path("massage_list/<int:pk>/edit/", views.massage_edit, name="massage_edit"),
    path("massage_list/<int:customer_pk>/add/", views.massage_add, name="massage_add"),
    path("logout", views.custom_logout, name="logout"),
    path(
        "report_hours_detail/<int:pk>/",
        views.report_hours_detail,
        name="report_hours_detail",
    ),
    path("report_hours", views.report_hours, name="report_hours"),
    path("reports", views.reports, name="reports"),
    path("", views.index, name="index"),
]
