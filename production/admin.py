from django.contrib import admin
from .models import *
from django.contrib.admin import DateFieldListFilter
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportActionMixin
from daterangefilter.filters import PastDateRangeFilter


class KomposisiBeanAdmin(ExportActionMixin, admin.ModelAdmin):
	list_display=(
		
		'tanggal_pembuatan_komposisi',
		'kode_komposisi',
		'komposisi_blend',
		'catatan'
)

admin.site.register(KomposisiBean, KomposisiBeanAdmin)

# class InlineProductioDiv(admin.StackedInline):
# 	model = ProductionDiv

# 	extra = 1

class ProductionDivAdmin(ExportActionMixin, admin.ModelAdmin):
	# inlines = [InlineProductioDiv]
	list_display = ('product_code','tanggal_blend','roast_date', 'nomor_set', 'jenis_blend', 'production_check_pass', 'cupping', 'qc_check_pass', 'pack_status', 'umur_blend')
	search_fields = ('tanggal_blend', 'jenis_blend')
	list_filter = (('tanggal_blend', PastDateRangeFilter),('roast_date', PastDateRangeFilter),'jenis_blend','cupping','production_check_pass', 'qc_check_pass',)
	prepopulated_fields = {'product_code':('blend_code', 'nomor_set','tanggal_blend')}

class ProductionSampleBlendAdmin(ExportActionMixin, admin.ModelAdmin):
	list_display = (
		
		'nama_blend',
		'kode_sample',
		'mesin',
		'production_date',
		'tanggal_pembuatan_sample',
		'diterima_qc',
		'penerima',
		 'catatan',
		 
		 )
	list_filter = (
		('tanggal_pembuatan_sample', PastDateRangeFilter),
		'nama_blend',
		'mesin',
		'kode_sample',
		
		'diterima_qc', 
		'catatan')

	prepopulated_fields = {'kode_sample':('nama_blend','mesin','production_date')}


class QCSampleBlendAdmin(ExportActionMixin, admin.ModelAdmin):
	list_display=(
		'blend_name',
		'sample_blend',
		'tanggal_diterima',
		'qc_acceptance',
		'catatan'

		)

	list_filter = (
		'blend_name',
		('tanggal_diterima', PastDateRangeFilter),
		'sample_blend',
		'qc_acceptance'


		)




admin.site.register(ProductionDiv, ProductionDivAdmin)
admin.site.register(BlendName)
admin.site.register(ProductionSampleBlend, ProductionSampleBlendAdmin)
admin.site.register(QCSampleBlend, QCSampleBlendAdmin)


