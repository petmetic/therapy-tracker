from django.shortcuts import render, get_object_or_404, redirect

from .models import Customer, Massage

from .forms import MassageForm


def index(request):
    return render(request, 'web/index.html', {})


def login(request):
    return render(request, 'web/login.html', {})


def customer_list(request):
    customers = Customer.objects.all()

    return render(request,
                  'web/customer_list.html',
                  {'customers_list': customers})


def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    massage_list = customer.massage_set.all()
    return render(request,
                  'web/customer_detail.html',
                  {'massage_list': massage_list, 'customer': customer})


def massage_detail(request, pk):
    massage = get_object_or_404(Massage, pk=pk)
    return render(request,
                  'web/massage_detail.html',
                  {'massage': massage})


def massage_add(request, customer_pk: int):
    customer = get_object_or_404(Customer, pk=customer_pk)

    if request.method == 'POST':
        form = MassageForm(request.POST)
        if form.is_valid():
            massage = form.save()
            return redirect(f'/massage_list/{massage.pk}/detail/')
    else:
        form = MassageForm()
    return render(request, 'web/massage_add.html', {'form': form})


def error(request):
    if error == "404":
        return render(request, 'web/404.html', {})

    else:
        return render(request, 'web/500.html', {})
