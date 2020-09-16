from django.contrib import admin
from django.shortcuts import render
from .models import *
from .forms import *
from django import forms
from django.contrib.admin import DateFieldListFilter
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportActionMixin
from daterangefilter.filters import PastDateRangeFilter
from django.contrib.auth import get_permission_codename
from django.forms.models import BaseInlineFormSet, ModelForm
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from django.db.models import Count
from django.db import models
import json
from products.models import Roaster
from django_admin_listfilter_dropdown.filters import ( DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter)

date = date.today()





class RunTimeStockResource(resources.ModelResource):


	blend_name = fields.Field(
		attribute='blend_name',
		column_name='blend_name',
		widget=ForeignKeyWidget(BlendName, 'nama_blend')
		)
	pack_size = fields.Field(attribute='pack_size',
		column_name='pack_size',
		widget=ForeignKeyWidget(Pack, 'pack_name')
		)
	stock_forecast_pack = fields.Field(attribute='stock_forecast_pack')
	stock_forecast_qty = fields.Field(attribute='stock_forecast_qty')
	stock_masuk_pack = fields.Field(attribute='stock_masuk_pack')
	stock_masuk_qty = fields.Field(attribute='stock_masuk_qty')
	forecast_vs_real_kg = fields.Field(attribute='forecast_vs_real_kg')
	forecast_vs_real_pcs = fields.Field(attribute='forecast_vs_real_pcs')
	forecast_vs_real_percentage = fields.Field(attribute='forecast_vs_real_percentage')
	stock_keluar_pack = fields.Field(attribute='stock_keluar_pack')
	stock_keluar_qty = fields.Field(attribute='stock_keluar_qty')
	stock_update_pack = fields.Field(attribute='stock_update_pack')
	pcs = fields.Field(attribute='pcs')
	stock_update_quantity = fields.Field(attribute='stock_update_quantity')	
	kg = fields.Field(attribute='kg')



class ProductionDivResource(resources.ModelResource):

	
	production_date = fields.Field(
		attribute='production_date',
		column_name='production_date',
		widget=ForeignKeyWidget(BlendReport, 'production_date')
		)

	product_code= fields.Field(attribute='product_code')	
	roast_date = fields.Field(attribute='roast_date')
	nomor_set = fields.Field(attribute='nomor_set')	
	komposisi = fields.Field(
		attribute='komposisi',
		column_name='komposisi',
		widget=ForeignKeyWidget(KomposisiBean, 'komposisi_blend')
		)	
	mesin = fields.Field(attribute='mesin')
	shift = fields.Field(attribute='shift')	
	pack_size = fields.Field(
		attribute='pack_size',
		column_name='beans_name',
		widget=ForeignKeyWidget(Pack, 'pack_name')
		)
	weight = fields.Field(attribute='weight')
	agtron_meter = fields.Field(attribute='agtron_meter')
	production_check_pass = fields.Field(attribute='production_check_pass')
	cupping = fields.Field(attribute='cupping')
	qc_check_pass = fields.Field(attribute='qc_check_pass')
	taste_notes = fields.Field(attribute='taste_notes')
	pack_status = fields.Field(attribute='pack_status')
	umur_blend = fields.Field(attribute='umur_blend')



class BlendReportResource(resources.ModelResource):


	production_date= fields.Field(attribute='production_date',)
	blend_id= fields.Field(attribute='blend_id',)
	blend_name= fields.Field(attribute='blend_name',
		column_name='blend_name',
		widget=ForeignKeyWidget(RunTimeStock, 'blend_name')
		)
	input_by= fields.Field(attribute='input_by',
		column_name='input_by',
		widget=ForeignKeyWidget(Karyawan, 'nama_lengkap')
		)
	blend_recorded= fields.Field(attribute='blend_recorded',)
	total_weight= fields.Field(attribute='total_weight')
	pack_size= fields.Field(attribute='pack_size',
		column_name='pack_size',
		widget=ForeignKeyWidget(Pack, 'pack_name')
		)
	perkiraan_jumlah_pack= fields.Field(attribute='perkiraan_jumlah_pack',)
	catatan_laporan= fields.Field(attribute='catatan_laporan')




class BarangKeluarResource(resources.ModelResource):

	
	tanggal_dan_jam = fields.Field(attribute='tanggal_dan_jam',)
	blend_name = fields.Field(
		attribute='blend_name',
		column_name='blend_name',
		widget=ForeignKeyWidget(RunTimeStock, 'blend_name')
		)
	invoice_number = fields.Field(attribute='invoice_number',)
	customer = fields.Field(
		attribute='customer',
		column_name='customer',
		widget=ForeignKeyWidget(DaftarCustomer, 'nama_customer')
		)
	jenis_pack = fields.Field(attribute='jenis_pack',
		column_name='jenis_pack',
		widget=ForeignKeyWidget(Pack, 'pack_name')
		)
	volume_pack = fields.Field(attribute='volume_pack',)
	volume_quantity = fields.Field(attribute='volume_quantity',)
	catatan = fields.Field(attribute='catatan',)




class PackFormInputResource(resources.ModelResource):


	tanggal_dan_jam = fields.Field(attribute='tanggal_dan_jam',)
	blend_name  = fields.Field(
		attribute='blend_name',
		column_name='blend_name',
		widget=ForeignKeyWidget(RunTimeStock, 'blend_name')
		)
	jenis_pack = fields.Field(
		attribute='jenis_pack',
		column_name='jenis_pack',
		widget=ForeignKeyWidget(Pack, 'pack_name')
		)
	volume_pack = fields.Field(attribute='volume_pack',)
	pcs = fields.Field(attribute='pcs',)
	volume_quantity = fields.Field(attribute='volume_quantity',)
	kg = fields.Field(attribute='kg',)
	catatan = fields.Field(attribute='catatan',)




class DaftarCustomerAdmin(ExportActionMixin, admin.ModelAdmin):


	list_display = (

	'nama_customer',
	'no_telp',
	'alamat',
	'pic', 
	'total_weight')




class PackFormInputAdmin(ExportActionMixin, admin.ModelAdmin):
	

	list_display = (

		'tanggal_dan_jam',
		'blend_name',
		'jenis_pack',
		'volume_quantity',
		'kg',
		'volume_pack',
		'pcs',
		'catatan'

		)
	resource_class = PackFormInputResource



class RunTimeStockAdmin(ExportActionMixin, admin.ModelAdmin):
	

	list_display = (

		'blend_name',
		'pack_size',
		'stock_forecast_pack',
		'pcs',
		'stock_forecast_qty',
		'kg',
		'stock_masuk_pack',
		'pcs',
		'stock_masuk_qty',
		'kg',
		'forecast_vs_real_kg',
		'forecast_vs_real_pcs',
		'forecast_vs_real_percentage',
		'stock_keluar_pack',
		'stock_keluar_qty',
		'stock_update_pack',
		'pcs',
		'stock_update_quantity',
		'kg'
		)

	
	list_filter = (
		'blend_name',
		'pack_size',
		)
	
	resource_class = RunTimeStockResource

class PackAdmin(ExportActionMixin, admin.ModelAdmin):
	

	list_display = (

	'pack_name', 
	'pack_volume',
	'pack_uom'

		)



class BarangKeluarAdmin(ExportActionMixin, admin.ModelAdmin):


	list_display= (

	'tanggal_dan_jam', 
	'blend_name',
	'invoice_number',
	'customer',
	'jenis_pack',
	'volume_pack',
	'volume_quantity',
	'catatan',

		)
	
	list_filter= (

		('tanggal_dan_jam', PastDateRangeFilter),
		'blend_name',
		'customer',
		'jenis_pack'

		)

	resource_class = BarangKeluarResource


class KomposisiBeanAdmin(ExportActionMixin, admin.ModelAdmin):


	list_display=(
		
		'tanggal_pembuatan_komposisi',
		'kode_komposisi',
		'komposisi_blend',
		'catatan',
		'jumlah_data'
)


admin.site.register(KomposisiBean, KomposisiBeanAdmin)


class ProductionDivInline(admin.StackedInline):


	model = ProductionDiv
	extra=0



class KaryawanAdmin(ExportActionMixin, admin.ModelAdmin):


	list_display =(

		'nama_panggilan',
		'nama_lengkap',
		'no_telp',
		'alamat' ,
		'status_aktif',
		)


class RoastedMaterialInline(admin.StackedInline):


	model = ProductionDiv.roasted_material.through
	extra = 1



class ProductionDivAdmin(ExportActionMixin, admin.ModelAdmin):


	


	# inlines = [InlineProductioDiv]
	list_display = ('id',
		'initial_create',
		'production_date',
		'nomor_set',
		'roast_date', 
		'roasted_material_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
		'roasting_shift', 
		'roasted_batch',
		'roasted_roastcode',
		'roasted_catatan',
		'product_code', 
		'komposisi',
		'weight',
		'total_weight',
		'kg',
		'catatan_blend',
		'catatan_produksi',
		'agtron_meter',
		'taste_notes',
		'production_check_pass', 
		'cupping', 'qc_check_pass',
		'pack_status', 
		'catatan_qc',
		'parent_id',
		'lead_time',
		'umur_blend',)

	readonly_fields = (
	'id',)
	search_fields = (
		'tanggal_blend',
		'jenis_blend'
	)
	# list_editable = ['cupping']
	list_filter = (
		('initial_create',PastDateRangeFilter),
		('roast_date', PastDateRangeFilter),
		'roasted_material',
		'production_date__blend_name_bulanan__blend_name',
		'mesin',
		('komposisi', RelatedDropdownFilter),
		'roasted_material__roaster',
		'cupping',
		'production_check_pass',
		'qc_check_pass',
	)

	exclude = ['cupping', 'qc_check_pass', 'taste_notes', 'pack_status', 'catatan_qc']


	list_editable = [
	'agtron_meter', 
	'taste_notes',
	'production_check_pass', 
	'cupping', 
	'qc_check_pass', 
	'pack_status',
	'catatan_qc',
	]

	list_max_show_all = 2500
	list_per_page = 20

	# form = ProductionDivAdminForm

	# inlines = [
	# 		RoastedMaterialInline
	# 	]

	# exclude = ('roasted_material',)
	formfield_overrides = {
		models.ManyToManyField: {'widget': forms.SelectMultiple(attrs={'size':'20', 'style': 'color:red;width:900px;height:400px','rows':7, 'cols':80})}
		# models.ManyToManyField: {'widget': .Textarea(attrs={'size':'20', 'style': 'color:red;width:450px;height:400px'})},
	}
	filter_horizontal = ('roasted_material',)

	list_display_links = None 
	resource_class = ProductionDivResource



	def changelist_view(self, request, extra_context=None):


		cup_task = ProductionDiv.objects.filter(cupping=False).count()
		karantina_produksi = ProductionDiv.objects.filter(production_check_pass=False).count()
		karantina_qc = ProductionDiv.objects.filter(qc_check_pass=False).count()
		unpack_status = ProductionDiv.objects.filter(pack_status=False).count()
		context = {
		'cup_task': cup_task,
		'karantina_produksi' : karantina_produksi,
		'karantina_qc' : karantina_qc,
		"unpack_status" : unpack_status
		}

		return super().changelist_view(request, extra_context=context)

	

class BlendReportAdmin(ExportActionMixin, admin.ModelAdmin):


	list_display = [
	'blend_id',
	'production_date',
	'blend_name',
	'input_by',
	'blend_recorded',
	'total_weight','uom',
	'pack_size',
	# 'perkiraan_jumlah_pack', #fix this !!!!
	'catatan_laporan',
	'agtron_avg',]

	list_filter = (('production_date', PastDateRangeFilter),
	'blend_name',
	'input_by',)

	inlines = [
		ProductionDivInline,
	]

	exclude = ('roasted_material',)

	resource_class = BlendReportResource

	# def changelist_view(self, request, extra_content=None):
	
	# 	chart_data = []
	# 	return super().changelist_view(request, extra_context=extra_context)






	



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



class DisposalItemInline(admin.StackedInline):


	model = DisposalItem
	extra=0



class DisposalReportAdmin(ExportActionMixin, admin.ModelAdmin):


	readonly_fields = ['id',]
	
	list_display=(
		'id',
		'tanggal_BAP',
		'author',
		'weight',
		'kg',
		'value',
		'unit',
		'note',
		'hard_copy_url',
		'diketahui_oleh'

		)

	list_filter =(
		('tanggal_BAP', PastDateRangeFilter),
		'author',)

	inlines = [
		DisposalItemInline
	]




class DisposalItemAdmin(ExportActionMixin, admin.ModelAdmin):


	list_display=(
			'report_id',
			# 'created', 
			'production_date',
			'material_name',
			'weight',
			'kg',
			'value_per_kg',
			'idr',
			'total_value',
			'idr',
			'note'
		)

	list_filter =(
		('production_date',PastDateRangeFilter),
		'material_name'
		)




class KejadianAdmin(ExportActionMixin, admin.ModelAdmin):


	list_display = (
		'tanggal',
		'reporter',
		'tingkat_urgensi',
		'kronologi',
		'resolusi' 
)

	list_filter = (
	('tanggal', PastDateRangeFilter),
	'reporter',
	'tingkat_urgensi',
	'kronologi',
	'resolusi' 
)




admin.site.register(ProductionDiv, ProductionDivAdmin)
admin.site.register(BlendName)
admin.site.register(ProductionSampleBlend, ProductionSampleBlendAdmin)
admin.site.register(QCSampleBlend, QCSampleBlendAdmin)
admin.site.register(Karyawan, KaryawanAdmin)
admin.site.register(BlendReport, BlendReportAdmin)
admin.site.register(Pack, PackAdmin)
admin.site.register(RunTimeStock, RunTimeStockAdmin)
admin.site.register(PackFormInput, PackFormInputAdmin)
admin.site.register(BarangKeluar, BarangKeluarAdmin)
admin.site.register(DaftarCustomer, DaftarCustomerAdmin)
admin.site.register(DisposalReport, DisposalReportAdmin)
admin.site.register(DisposalItem, DisposalItemAdmin)
admin.site.register(Kejadian, KejadianAdmin)