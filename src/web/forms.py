from django.forms import ModelForm

from .models import Massage, Customer

from django.core.exceptions import ValidationError


class MassageForm(ModelForm):
    class Meta:
        model = Massage
        exclude = ["added", "changed"]


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = [
            "name",
            "surname",
            "email",
            "phone",
            "occupation",
            "previous_massage",
            "salon_choice",
            "frequency",
            "referral",
        ]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data["name"]
        surname = cleaned_data["surname"]
        email = cleaned_data["email"]
        phone = cleaned_data["phone"]
        customer = Customer.objects.filter(
            name=name, surname=surname, email=email, phone=phone
        ).first()
        if customer:
            raise ValidationError(
                "Customer already exists in database. Please check for correct input in fields."
            )
        return cleaned_data
