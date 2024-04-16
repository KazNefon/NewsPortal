from django import forms
from .models import Category

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = []
