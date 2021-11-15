from django import forms
from .models import Rent

class RentCreateForm(forms.ModelForm):
    class Meta:
        model = Rent
        fields = ['name', 'email', 'address', 'detailadd', 'phone']