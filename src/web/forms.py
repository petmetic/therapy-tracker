from django.forms import ModelForm

from django import forms

from .models import Massage, Customer

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.forms import AuthenticationForm


class MassageForm(ModelForm):
    start = forms.DateTimeField(
        label=_("Time of visit"),
        label_suffix="",
        widget=forms.DateInput(
            format="%Y-%m-%d %H:%M:%S",
            attrs={"class": "form-control", "type": "datetime-local"},
        ),
    )

    reason_for_visit = forms.CharField(
        label=_("Reason for visit"),
        label_suffix="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": _("back pain"),
            }
        ),
    )
    kind = forms.CharField(
        label=_("Type of massage preformed"),
        label_suffix="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": _("pain relief"),
            }
        ),
    )
    notes = forms.CharField(
        label=_("Massage notes"),
        label_suffix="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": _("please write what you did for customer"),
            }
        ),
    )
    next_visit = forms.CharField(
        label=_("Massage at next visit"),
        label_suffix="",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": _("please write what you are going to do on next visit"),
            }
        ),
    )
    recommendations = forms.CharField(
        label=_("Recommendations"),
        label_suffix="",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": _(
                    "please write what exercises the customer does at home to speed up recovery"
                ),
            }
        ),
    )
    personal_notes = forms.CharField(
        label=_("Personal notes"),
        label_suffix="",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "type": "text"}),
    )

    duration = forms.IntegerField(
        label=_("Duration of massage"),
        label_suffix="",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "placeholder": _(
                    "please write how long did the massage take in minutes"
                ),
            }
        ),
    )

    amount = forms.IntegerField(
        label=_("Amount paid"),
        label_suffix="",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "placeholder": _("please write the actual value of massage in euro"),
            }
        ),
    )

    discount = forms.IntegerField(
        label=_("Discount"),
        label_suffix="",
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "placeholder": _("please write the discount in %"),
            }
        ),
    )

    discount_reason = forms.CharField(
        label=_("Reason for discount"),
        label_suffix="",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "type": "text"}),
    )

    repeat_visit = forms.BooleanField(
        label=_("Repeat visit"),
        label_suffix="",
        required=False,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "type": "checkbox"}
        ),
    )

    class Meta:
        model = Massage
        exclude = [
            "added",
            "changed",
            "service",
            "external_id",
            "status",
            "end",
        ]

    def clean(self):
        cleaned_data = super().clean()
        discount = cleaned_data["discount"]
        discount_reason = cleaned_data["discount_reason"]

        if discount and not discount_reason:
            raise ValidationError(_("Please fill in Reason for discount."))

        return cleaned_data


class MassageEditForm(ModelForm):
    start = forms.DateTimeField(
        label=_("Time of visit"),
        label_suffix="",
        widget=forms.DateTimeInput(
            format="%Y-%m-%d %H:%M:%S",
            attrs={"class": "form-control", "type": "datetime-local"},
        ),
    )
    reason_for_visit = forms.CharField(
        label=_("Reason for visit"),
        label_suffix="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": _("back pain"),
            }
        ),
    )
    kind = forms.CharField(
        label=_("Type of massage preformed"),
        label_suffix="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": _("pain relief"),
            }
        ),
    )
    notes = forms.CharField(
        label=_("Massage preformed"),
        label_suffix="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": _("please write what you did for customer"),
            }
        ),
    )
    next_visit = forms.CharField(
        label=_("Massage at next visit"),
        label_suffix="",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": _("please write what you are going to do on next visit"),
            }
        ),
    )
    recommendations = forms.CharField(
        label=_("Recommendations"),
        label_suffix="",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": _(
                    "please write what exercises the customer does at home to speed up recovery"
                ),
            }
        ),
    )
    personal_notes = forms.CharField(
        label=_("Personal notes"),
        label_suffix="",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "type": "text"}),
    )

    duration = forms.IntegerField(
        label=_("Duration of massage"),
        label_suffix="",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "placeholder": _(
                    "please write how long did the massage take in minutes"
                ),
            }
        ),
    )

    amount = forms.IntegerField(
        label=_("Amount paid"),
        label_suffix="",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "placeholder": _("please write the actual value of massage in euro"),
            }
        ),
    )

    discount = forms.IntegerField(
        label=_("Discount"),
        label_suffix="",
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "placeholder": _("please write the discount in %"),
            }
        ),
    )

    discount_reason = forms.CharField(
        label=_("Reason for discount"),
        label_suffix="",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "type": "text"}),
    )

    repeat_visit = forms.BooleanField(
        label=_("Repeat visit"),
        label_suffix="",
        required=False,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "type": "checkbox"}
        ),
    )

    main_concern = forms.CharField(
        label=_("Main concern"),
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": _("car accident"),
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["therapist"].widget = forms.HiddenInput()

    class Meta:
        model = Massage
        exclude = [
            "added",
            "changed",
            "service",
            "status",
            "end",
            "customer",
            "external_id",
        ]


class CustomerForm(ModelForm):
    name = forms.CharField(
        label=_("Name"),
        label_suffix="",
        widget=forms.TextInput(attrs={"class": "form-control", "type": "text"}),
    )
    surname = forms.CharField(
        label=_("Surname"),
        label_suffix="",
        widget=forms.TextInput(attrs={"class": "form-control", "type": "text"}),
    )
    email = forms.EmailField(
        label=_("Email"),
        label_suffix="",
        widget=forms.EmailInput(attrs={"class": "form-control", "type": "email"}),
    )
    phone = forms.CharField(
        label=_("Phone"),
        label_suffix="",
        widget=forms.TextInput(attrs={"class": "form-control", "type": "text"}),
    )
    occupation = forms.CharField(
        label=_("Occupation"),
        label_suffix="",
        widget=forms.TextInput(attrs={"class": "form-control", "type": "text"}),
    )

    previous_massage = forms.BooleanField(
        label=_("Previous massage"),
        label_suffix="",
        required=False,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "type": "checkbox"}
        ),
    )
    salon_choice = forms.CharField(
        label=_("Why did they choose our salon?"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": _("reason for choosing our salon"),
            }
        ),
    )

    frequency = forms.CharField(
        label=_("How frequently do they visit a massage salon?"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": _("3x times a week"),
            }
        ),
    )

    referral = forms.CharField(
        label=_("Where did the customer find us?"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": _("friend recommendations"),
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
                _(
                    "Customer already exists in database. Please check for correct input in fields."
                )
            )
        return cleaned_data


class CustomerEditForm(ModelForm):
    name = forms.CharField(
        label=_("Name"),
        label_suffix="",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "type": "text"}),
    )
    surname = forms.CharField(
        label=_("Surname"),
        label_suffix="",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "type": "text"}),
    )
    email = forms.EmailField(
        label=_("Email"),
        label_suffix="",
        required=False,
        widget=forms.EmailInput(attrs={"class": "form-control", "type": "email"}),
    )
    phone = forms.CharField(
        label=_("Phone"),
        label_suffix="",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "type": "text"}),
    )
    occupation = forms.CharField(
        label=_("Occupation"),
        label_suffix="",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "type": "text"}),
    )
    previous_massage = forms.BooleanField(
        label=_("Previous massage"),
        label_suffix="",
        required=False,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "type": "checkbox"}
        ),
    )
    salon_choice = forms.CharField(
        label=_("Why did they choose our salon?"),
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": _("reason for choosing our salon"),
            }
        ),
    )

    frequency = forms.CharField(
        label=_("How frequently do they visit a massage salon?"),
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": _("3x times a week"),
            }
        ),
    )

    referral = forms.CharField(
        label=_("Where did the customer find us?"),
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": _("friend recommendations"),
            }
        ),
    )

    main_concern = forms.CharField(
        label=_("Main concern"),
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": _("car accident"),
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
            "main_concern",
        ]


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {"placeholder": _("Username"), "class": "form-control"}
        )
        self.fields["password"].widget.attrs.update(
            {"placeholder": _("Password"), "class": "form-control"}
        )
