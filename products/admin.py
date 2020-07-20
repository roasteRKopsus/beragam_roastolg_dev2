
from django.contrib import admin

from .models import *
from import_export.admin import ExportActionMixin
from daterangefilter.filters import PastDateRangeFilter
from django_admin_listfilter_dropdown.filters import ( DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter)
from django.db.models import Sum, Avg
from admin_totals.admin import ModelAdminTotals

from django.contrib.admin.views.main import ChangeList



class QCSampleBeanAdmin(ExportActionMixin, admin.ModelAdmin):
	list_display =(
		'sample_code','sample_date','cupping_date','biji','jenis_kopi','Crop_year', 'vendor_name','total_score')
	list_filter=('sample_code',('sample_date', PastDateRangeFilter),'cupping_date','biji','jenis_kopi','Crop_year', 'vendor_name','total_score')

class BeansGudangAdmin(ExportActionMixin, admin.ModelAdmin):
	list_display = ('sample_code','biji','vendor_name', 'lot_number', 'bag_amount','berat_kopi_in_kg', 'qc_acceptance')





class RoasterAdmin(ExportActionMixin, ModelAdminTotals, admin.ModelAdmin):
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

	list_totals = [('berat_akhir', lambda field: Coalesce(Sum(field), 0)), ('persentase_susut', Avg)]



admin.site.register(BeansGudang, BeansGudangAdmin)
admin.site.register(Roaster, RoasterAdmin)
admin.site.register(QCSampleBean, QCSampleBeanAdmin)

