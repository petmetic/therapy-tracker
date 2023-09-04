import datetime
import pytz

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required

from .models import Customer, Massage

from .forms import (
    MassageForm,
    CustomerForm,
    MassageEditForm,
    CustomerEditForm,
    CustomAuthenticationForm,
)

tz = pytz.timezone("Europe/Ljubljana")


@login_required
def index(request):
    therapist = request.user
    today = datetime.datetime.now()
    massages = (
        Massage.objects.filter(
            therapist=therapist,
            start__year=today.year,
            start__month=today.month,
            start__day=today.day,
            status="approved",
        )
        .select_related("customer")
        .order_by("start")
    )

    return render(
        request,
        "web/index.html",
        {
            "therapist": therapist,
            "massages": massages,
            "today": today,
        },
    )


@login_required
def customer_list(request):
    customers = Customer.objects.all().order_by("surname")

    return render(request, "web/customer_list.html", {"customers_list": customers})


@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    massage_list = customer.massage_set.filter(
        status="approved",
        start__lte=datetime.datetime.now(),
    )
    return render(
        request,
        "web/customer_detail.html",
        {"massage_list": massage_list, "customer": customer},
    )


@login_required
def customer_add(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            return redirect(reverse("customer", kwargs={"customer_pk": customer.pk}))

    else:
        form = CustomerForm()
    return render(request, "web/customer_add.html", {"form": form})


@login_required
def customer(request, customer_pk: int):
    customer = get_object_or_404(Customer, pk=customer_pk)
    return render(request, "web/customer.html", {"customer": customer})


@login_required
def customer_edit(request, customer_pk: int):
    customer = get_object_or_404(Customer, pk=customer_pk)

    if request.method == "POST":
        form = CustomerEditForm(
            request.POST,
            instance=customer,
            initial={
                "customer": customer,
            },
        )
        if form.is_valid():
            customer = form.save()
            return redirect(reverse("customer", kwargs={"customer_pk": customer.pk}))
        else:
            print(form.errors)
    else:
        form = CustomerEditForm(instance=customer, initial={"customer": customer})
    return render(
        request,
        "web/customer_edit.html",
        {"form": form, "customer": customer},
    )


@login_required
def massage_detail(request, pk: int):
    massage = get_object_or_404(Massage, pk=pk)
    return render(
        request,
        "web/massage_detail.html",
        {"massage": massage, "therapist": request.user},
    )


@login_required
def massage_add(request, customer_pk: int):
    customer = get_object_or_404(Customer, pk=customer_pk)
    if request.method == "POST":
        form = MassageForm(
            request.POST, initial={"customer": customer, "therapist": request.user}
        )
        if form.is_valid():
            massage = form.save()
            return redirect(reverse("massage_detail", kwargs={"pk": massage.pk}))
        # else:
        #     print(form.errors)
    else:
        form = MassageForm(initial={"customer": customer, "therapist": request.user})
    return render(
        request,
        "web/massage_add.html",
        {"form": form, "customer": customer, "therapist": request.user},
    )


@login_required
def massage_edit(request, pk: int):
    massage = get_object_or_404(Massage, pk=pk)
    if not request.user == massage.therapist:
        raise PermissionDenied
    customer = massage.customer

    if request.method == "POST":
        form = MassageEditForm(
            request.POST,
            instance=massage,
            initial={
                "massage": massage,
                "therapist": request.user,
                "customer": customer,
                "main_concern": customer.main_concern,
            },
        )

        if form.is_valid():
            massage = form.save()
            customer.main_concern = form.cleaned_data.get("main_concern")
            customer.save()
            return redirect(reverse("massage_detail", kwargs={"pk": massage.pk}))
        else:
            print(form.errors)
    else:
        form = MassageEditForm(
            instance=massage,
            initial={
                "customer": customer,
                "therapist": request.user,
                "main_concern": customer.main_concern,
            },
        )
    return render(
        request,
        "web/massage_edit.html",
        {"form": form, "massage": massage, "therapist": request.user},
    )


@staff_member_required
def reports(request):
    start_date = request.GET.get("start-date")
    end_date = request.GET.get("end-date")

    return render(
        request, "web/reports.html", {"start_date": start_date, "end_date": end_date}
    )


@staff_member_required
def report_hours(request):
    therapists = (
        User.objects.all()
        .exclude(first_name="Meta")
        .exclude(username="meta")
        .order_by("first_name")
    )
    return render(request, "web/report_hours.html", {"therapist_list": therapists})


@staff_member_required
def report_hours_detail(request, pk: int):
    therapist = get_object_or_404(User, pk=pk)
    massages = Massage.objects.filter(therapist=therapist)
    amount = 0
    for massage in massages:
        amount += massage.service.payout

    return render(
        request,
        "web/report_hours_detail.html",
        {"therapist": therapist, "massages": massages, "amount": amount},
    )


def custom_logout(request):
    logout(request)
    return redirect("/")


def error(request):
    if error == "404":
        return render(request, "web/404.html", {})

    else:
        return render(request, "web/500.html", {})


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
