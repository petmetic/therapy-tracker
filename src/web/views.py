from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Customer, Massage

from .forms import MassageForm, CustomerForm


@login_required
def index(request):
    return render(request, "web/index.html", {})


@login_required
def customer_list(request):
    customers = Customer.objects.all()

    return render(request, "web/customer_list.html", {"customers_list": customers})


@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    massage_list = customer.massage_set.all()
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
            return redirect(reverse("customer_detail", kwargs={"pk": customer.pk}))

    else:
        form = CustomerForm()
    return render(request, "web/customer_add.html", {"form": form})


@login_required
def massage_detail(request, pk):
    massage = get_object_or_404(Massage, pk=pk)
    return render(request, "web/massage_detail.html", {"massage": massage})


@login_required
def massage_add(request, customer_pk: int):
    customer = get_object_or_404(Customer, pk=customer_pk)
    if request.method == "POST":
        form = MassageForm(request.POST)
        if form.is_valid():
            massage = form.save()
            return redirect(reverse("massage_detail", kwargs={"pk": massage.pk}))
    else:
        form = MassageForm()
    return render(request, "web/massage_add.html", {"form": form})


def custom_logout(request):
    logout(request)
    return redirect("/")


def error(request):
    if error == "404":
        return render(request, "web/404.html", {})

    else:
        return render(request, "web/500.html", {})
