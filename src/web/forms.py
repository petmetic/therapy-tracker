from django.forms import ModelForm

from .models import Massage, Customer


class MassageForm(ModelForm):
    class Meta:
        model = Massage
        exclude = ['added', 'changed']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

