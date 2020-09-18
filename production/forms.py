from django import forms

from django.db import models
from .models import *
from products.models import Roaster
from django.contrib import admin



# class ProductionDivForm(forms.ModelForm):
# 	tanggal_blend = forms.DateField(widget=forms.TextInput(attrs=
#                                 {
#                                     'class':'datepicker'
#                                 }))
# 	class Meta:
# 		model = ProductionDiv
# 		fields = '__all__'
# 		# widgets = {
# 		# 	'roasted_material' : admin.widgets.SelectMultiple
# 		# }

class ProductionDivAdminForm(forms.ModelForm):
	roasted_material = forms.ModelMultipleChoiceField(
			queryset = Roaster.objects.filter(next_process =False),
			widget = forms.SelectMultiple
			)
	def __init__(self, *args, **kwargs):
		if kwargs.get('instance'):
			initial = kwargs.setdefault('initial', {})
			initial['roasted_material'] = [t.pk for t in kwargs['instance'].roasted_material.all()]
		forms.ModelForm.__init__(self, *args, **kwargs)

	def save(self, commit=True):
		instance = forms.ModelForm.save(self, False)
		old_save_m2m = self.save_m2m

		def save_m2m():
			old_save_m2m()
			instance.roasted_material_set.clear()
			instance.roasted_material_set.add(*self.cleaned_data['roasted_material'])
			self.save_m2m = save_m2m

		if commit:
			instance.save()
			self.save_m2m()

		return instance











	# class Meta:
	# 	model = ProductionDiv
