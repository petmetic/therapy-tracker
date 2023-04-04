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
        ),
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
        required=False,
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
        required=False,
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
        required=False,
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
        required=False,
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
        required=False,
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

    # def clean(self):
    #     cleaned_data = super().clean()
    #     massage_date = cleaned_data["massage_date"]
    #     reason_for_visit = cleaned_data["reason_for_visit"]
    #     kind = cleaned_data["kind"]
    #     massage_notes = cleaned_data["next_visit"]
    #     recommendations = cleaned_data["recommendations"]
    #     personal_notes = cleaned_data["personal_notes"]
    #     duration = cleaned_data["duration"]
    #     amount = cleaned_data["amount"]
    #     discount = cleaned_data["discount"]
    #     discount_reason = cleaned_data["discount_reason"]
    #     repeat_visit = cleaned_data["repeat_visit"]
    #
    #     # massage = Massage.objects.filter(
    #     #     customer=customer, therapist=therapist, massage_date=massage_date, reason_for_visit=reason_for_visit,
    #     #     kind=kind, massage_notes=massage_notes, recommendations=recommendations, personal_notes=personal_notes,
    #     #     duration=duration, discount=discount, amount=amount, discount_reason=discount_reason,
    #     #     repeat_visit=repeat_visit
    #     # ).first()
    #     # if massage.discount:
    #     #     massage.discount_reason(required=True)
    #     print(discount)
    #     print(discount_reason)
    #     if discount and not discount_reason:
    #         print('foo')
    #         raise ValidationError(
    #             "Please fill in the discount reason."
    #         )
    #
    #     return cleaned_data


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
