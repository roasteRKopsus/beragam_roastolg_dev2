
from django.contrib import admin

from .models import *
from import_export.admin import ExportActionMixin
from daterangefilter.filters import PastDateRangeFilter
from django_admin_listfilter_dropdown.filters import ( DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter)
from django.db.models import Sum, Avg
from django.db.models import Count, Sum
from django.contrib.admin.views.main import ChangeList



class QCSampleBeanAdmin(ExportActionMixin, admin.ModelAdmin):
	list_display =(
		'sample_code','sample_date','cupping_date','biji','jenis_kopi','Crop_year', 'vendor_name','total_score')
	list_filter=('sample_code',('sample_date', PastDateRangeFilter),'cupping_date','biji','jenis_kopi','Crop_year', 'vendor_name','total_score')

class BeansGudangAdmin(ExportActionMixin, admin.ModelAdmin):
	list_display = ('sample_code','biji','vendor_name', 'lot_number', 'bag_amount','berat_kopi_in_kg', 'qc_acceptance')

class MyChangeList(ChangeList):

	def get_results(self, *args, **kwargs):
		super(MyChangeList, self).get_results(*args, **kwargs)
		q = self.result_list.aggregate(total_berat_akhir=Sum('berat_akhir'))
		self.berat_akhir_count = q['total_berat_akhir']



class RoasterAdmin(ExportActionMixin, admin.ModelAdmin):

	def get_changelist(self, request):
    	return MyChangeList

	class Meta:
		model = Roaster

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



admin.site.register(BeansGudang, BeansGudangAdmin)
admin.site.register(Roaster, RoasterAdmin)
admin.site.register(QCSampleBean, QCSampleBeanAdmin)

