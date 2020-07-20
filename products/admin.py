
from django.contrib import admin

from .models import *
from import_export.admin import ExportActionMixin
from daterangefilter.filters import PastDateRangeFilter
from django_admin_listfilter_dropdown.filters import ( DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter)
from django.contrib.admin.views.main import ChangeList
from django.db.models import Sum, Avg


class QCSampleBeanAdmin(ExportActionMixin, admin.ModelAdmin):
	list_display =(
		'sample_code','sample_date','cupping_date','biji','jenis_kopi','Crop_year', 'vendor_name','total_score')
	list_filter=('sample_code',('sample_date', PastDateRangeFilter),'cupping_date','biji','jenis_kopi','Crop_year', 'vendor_name','total_score')

class BeansGudangAdmin(ExportActionMixin, admin.ModelAdmin):
	list_display = ('sample_code','biji','vendor_name', 'lot_number', 'bag_amount','berat_kopi_in_kg', 'qc_acceptance')





class TotalAveragesChangeList(ChangeList):
	fields_to_total = ['berat_akhir','berat_masuk', 'persentase_susut']

	def get_total_values(self, queryset):
		total =  Roaster()
		total.custom_alias_name = "Totals"
		for field in self.fields_to_total:
			setattr(total, field, queryset.aggregate(Sum(field)).items()[0][1])
		return total

	def get_average_values(self, queryset):
		average =  Roaster()
		average.custom_alias_name = "Averages"
		for field in self.fields_to_total:
			setattr(average, field, queryset.aggregate(Avg(field)).items()[0][1])
		return average

	def get_results(self, request):
		super(TotalAveragesChangeList, self).get_results(request)
		total = self.get_total_values(self.query_set)
		average = self.get_average_values(self.query_set)
		len(self.result_list)
		self.result_list._result_cache.append(total)
		self.result_list._result_cache.append(average)



class RoasterAdmin(ExportActionMixin, admin.ModelAdmin):

	def get_changelist(self, request, **kwargs):
		return TotalAveragesChangeList

	list_display = ('roast_date',
'beans_name',
'mesin',
'batch_number',
'berat_masuk',
'berat_akhir',
'persentase_susut',
'roaster_pass_check',
'catatan_roaster',
'umur_roastbean')


	
	list_filter=(('roast_date', PastDateRangeFilter),'mesin','roaster_pass_check', ('beans_name', RelatedDropdownFilter))
	# prepopulated_fields = {'susut':('persentase_susut')}
	#change_list_template = None
	#total = Roaster.objects.aggregate(Sum( 'berat_akhir'))

	


admin.site.register(BeansGudang, BeansGudangAdmin)
admin.site.register(Roaster, RoasterAdmin)
admin.site.register(QCSampleBean, QCSampleBeanAdmin)

