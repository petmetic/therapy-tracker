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
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": "pain relief",
            }
        ),
    )
    massage_notes = forms.CharField(
        label="Massage preformed:",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": "please write what you did for customer",
            }
        ),
    )
    next_visit = forms.CharField(
        label="Massage at next visit:",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": "please write what you are going to do on next visit",
            }
        ),
    )
    recommendations = forms.CharField(
        label="Recommendations:",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": "please write what excersizes the customer does at home to speed up recovery",
            }
        ),
    )
    personal_notes = forms.CharField(
        label="Personal notes:",
        widget=forms.Textarea(attrs={"class": "form-control", "type": "text"}),
    )

    duration = forms.CharField(
        label="Duration of massage:",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": "please write how long did the massage take in minutes",
            }
        ),
    )

    amount = forms.CharField(
        label="Amount paid:",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": "please write the actual value of massage in euro",
            }
        ),
    )

    discount = forms.CharField(
        label="Discount:",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": "please write the discount in %",
            }
        ),
    )

    discount_reason = forms.CharField(
        label="Reason for discount:",
        widget=forms.TextInput(attrs={"class": "form-control", "type": "text"}),
    )

    repeat_visit = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "type": "checkbox"}
        ),
    )

    class Meta:
        model = Massage
        exclude = ["added", "changed"]


class CustomerForm(ModelForm):
    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(attrs={"class": "form-control", "type": "text"}),
    )
    surname = forms.CharField(
        label="Surname",
        widget=forms.TextInput(attrs={"class": "form-control", "type": "text"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "type": "email"}),
    )
    phone = forms.CharField(
        label="Phone",
        widget=forms.TextInput(attrs={"class": "form-control", "type": "text"}),
    )
    occupation = forms.CharField(
        label="Occupation",
        widget=forms.TextInput(attrs={"class": "form-control", "type": "text"}),
    )
    previous_massage = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "type": "checkbox"}
        ),
    )
    salon_choice = forms.CharField(
        label="Why did they choose our salon?",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": "reason for choosing our salon",
            }
        ),
    )

    frequency = forms.CharField(
        label="How frequently do they visit a massage salon?",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": "3x times a week",
            }
        ),
    )

    referral = forms.CharField(
        label="Where did the customer find us?",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": "friend recommendations",
            }
        ),
    )

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
