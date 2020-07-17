from django import forms

from django.db import models
from .models import ProductionDiv



class ProductionDivForm(forms.ModelForm):
	tanggal_blend = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
	class Meta:
		model = ProductionDiv
		fields = '__all__'