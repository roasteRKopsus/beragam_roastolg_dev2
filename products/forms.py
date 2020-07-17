from django import forms

from django.db import models
from .models import Roaster

class RoasterForm(forms.ModelForm):
    stock_lot = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
    class Meta:
        model = Roaster
        fields = '__all__'



        
