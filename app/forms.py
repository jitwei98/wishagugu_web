from django import forms

from .models import Recipient


class RecipientInformationForm(forms.Form):
    name = forms.CharField()
    relationship = forms.CharField()
    interests = forms.CharField()
    gifting_context = forms.CharField()
    budget = forms.DecimalField()

class RecipientModelForm(forms.ModelForm):
    class Meta:
        model = Recipient
        exclude = ['gift_has_been_bought']

