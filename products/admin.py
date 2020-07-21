
from django.contrib import admin

from .models import *
from import_export.admin import ExportActionMixin
from daterangefilter.filters import PastDateRangeFilter
from django_admin_listfilter_dropdown.filters import ( DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter)
from django.db.models import Sum, Avg
from django.db.models.functions import Coalesce
from import_export import resources
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from django.contrib.admin.views.main import ChangeList
from django.db.models import Count, Sum


class QCSampleBeanAdmin(ExportActionMixin, admin.ModelAdmin):
	list_display =(
		'sample_code','sample_date','cupping_date','biji','jenis_kopi','Crop_year', 'vendor_name','total_score')
	list_filter=('sample_code',('sample_date', PastDateRangeFilter),'cupping_date','biji','jenis_kopi','Crop_year', 'vendor_name','total_score')

class BeansGudangAdmin(ExportActionMixin, admin.ModelAdmin):
	list_display = ('sample_code','biji','vendor_name', 'lot_number', 'bag_amount','berat_kopi_in_kg', 'qc_acceptance')

class TotalAveragesChangeList(ChangeList):

	fields_to_total = ['berat_akhir', 'berat_masuk']

	def get_total_values(self, queryset):
	"""
	Get the totals
	"""
	#basically the total parameter is an empty instance of the given model
		total =  Roaster()
		total.custom_alias_name = "Totals" 
		for field in self.fields_to_total:
	    	setattr(total, field, queryset.aggregate(Sum(field)).items()[0][1])
		return total

	def get_results(self, request):
		super(TotalAveragesChangeList, self).get_results(request)
		total = self.get_total_values(self.query_set)
		len(self.result_list)
		self.result_list._result_cache.append(total)

class RoasterResource(resources.ModelResource):
	beans_name = fields.Field(
        column_name='beans_name',
        attribute='beans_name',
        widget=ForeignKeyWidget(BeansGudang, 'biji'))

	class Meta:
		model = Roaster
	
	def get_changelist(self, request, **kwargs):
		return TotalAveragesChangeList

class RoasterAdmin(ExportActionMixin, admin.ModelAdmin):
	list_display = ('roast_date',
'beans_name',
'mesin',
'shift',
'batch_number',
'moisture_content',
'berat_masuk',
'berat_akhir',
'persentase_susut',
'roaster_pass_check',
'catatan_roaster',
'umur_roastbean')


	
	list_filter=(('roast_date', PastDateRangeFilter),'mesin','shift','roaster_pass_check', ('beans_name', RelatedDropdownFilter))
	# prepopulated_fields = {'susut':('persentase_susut')}

	resource_class = RoasterResource

admin.site.register(BeansGudang, BeansGudangAdmin)
admin.site.register(Roaster, RoasterAdmin)
admin.site.register(QCSampleBean, QCSampleBeanAdmin)

