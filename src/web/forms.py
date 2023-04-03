from django.forms import ModelForm

from django import forms

from .models import Massage, Customer

from django.core.exceptions import ValidationError


class MassageForm(ModelForm):
    massage_date = forms.DateTimeField(
        label="Date of visit:",
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "datetime-local"}
        ),
    )
    reason_for_visit = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "type": "text", "placeholder": "back pain"}
        )
    )
    kind = forms.CharField(
        label="Type of massage preformed:",
        widget=forms.TextInput(attrs={"class": "form-control", "type": "text"}),
    )
    massage_notes = forms.CharField(
        label="Massage preformed by:",
        widget=forms.Textarea(attrs={"class": "form-control", "type": "text"}),
    )
    next_visit = forms.CharField(
        label="Massage at next visit:",
        widget=forms.Textarea(attrs={"class": "form-control", "type": "text"}),
    )
    recommendations = forms.CharField(
        label="Recommendations:",
        widget=forms.Textarea(attrs={"class": "form-control", "type": "text"}),
    )
    repeat_visit = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "type": "checkbox"}
        )
    )

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
