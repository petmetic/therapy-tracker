from django.forms import ModelForm

from web.models import Massage


class MassageForm(ModelForm):
    class Meta:
        model = Massage
        exclude = ['added', 'changed']
