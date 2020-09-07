
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
from datetime import date
today = datetime.date.today()


class BeansCodeResource(resources.ModelResource):


	code = fields.Field(attribute='code')
	beans_name = fields.Field(attribute='beans_name')
	jenis_kopi = fields.Field(attribute='jenis_kopi')
	variety = fields.Field(attribute='variety')
	origin = fields.Field(attribute='origin')
	paska_panen = fields.Field(attribute='paska_panen')
	vendor_name = fields.Field(attribute='vendor_name')
	stock_terupdate = fields.Field(attribute='stock_terupdate')
	nilai_stock = fields.Field(attribute='nilai_stock')


class RoasterResource(resources.ModelResource):


	roast_date = fields.Field(attribute='roast_date')
	beans_name = fields.Field(
		attribute='beans_name',
		column_name='beans_name',
		widget=ForeignKeyWidget(BeansGudang, 'beans_name')
		)
	mesin = fields.Field(attribute='mesin')
	shift = fields.Field(attribute='shift')
	process = fields.Field(attribute='process')
	batch_number= fields.Field(attribute='batch_number')
	beans_color = fields.Field(attribute='beans_color')
	density = fields.Field(attribute='density')
	moisture = fields.Field(attribute='moisture_content')
	raw = fields.Field(attribute='raw')
	roasted = fields.Field(attribute='roasted')
	persentase_susut = fields.Field(attribute='persentase_susut')
	roaster_pass_check = fields.Field(attribute='roaster_pass_check')
	catatan_roaster = fields.Field(attribute='catatan_roaster')	
	umur_roastbean = fields.Field(attribute='umur_roastbean')



class PengambilanGreenbeanResource(resources.ModelResource):


	beans_name = fields.Field(
        column_name='beans_name',
        attribute='beans_name',
        widget=ForeignKeyWidget(BeansGudang, 'beans_name'))

	class Meta:
		model = PengambilanGreenbean


class BeansGudangResource(resources.ModelResource):


	last_update = fields.Field(attribute='last_update')
	sample_code = fields.Field(
		attribute='sample_code',
		column_name='beans_name',
		widget=ForeignKeyWidget(BeansCode, 'sample_code')
		)
	beans_name = fields.Field(attribute='beans_name')
	jenis_kopi = fields.Field(attribute='jenis_kopi')
	variety = fields.Field(attribute='variety')
	origin =  fields.Field(attribute='origin')
	paska_panen = fields.Field(attribute='paska_panen') 
	crop_year = fields.Field(attribute='Crop_year')
	vendor_name = fields.Field(attribute='vendor_name')
	lot_number  = fields.Field(attribute='lot_number')
	bag =  fields.Field(attribute='bag')
	qty_bag = fields.Field(attribute='qty_bag')
	inherited_stock = fields.Field(attribute='inherited_stock')
	initial_stock = fields.Field(attribute='initial_stock')
	price_kilo_idr = fields.Field(attribute='price_kilo_idr')
	stock_status = fields.Field(attribute='stock_status')
	stock_update = fields.Field(attribute='stock_update')
	beans_usage_amount = fields.Field(attribute='beans_usage_amount')
	beans_usage_value = fields.Field(attribute='beans_usage_value')
	beans_usage_percent = fields.Field(attribute='beans_usage_percent')
	depreciation_average = fields.Field(attribute='depreciation_average')
	roasted = fields.Field(attribute='roasted')
	qc_acceptance = fields.Field(attribute='qc_acceptance')
	moisture_check = fields.Field(attribute='moisture_check')
	primary_defect = fields.Field(attribute='primary_defect')
	secondary_defect = fields.Field(attribute='secondary_defect')
	aroma_greenbean = fields.Field(attribute='aroma_greenbean')
	fragrance_score = fields.Field(attribute='fragrance_score')
	fragrance_intensity = fields.Field(attribute='fragrance_intensity')
	fragrance_notes = fields.Field(attribute='fragrance_notes')
	flavor_score = fields.Field(attribute='flavor_score')
	flavor_intensity = fields.Field(attribute='flavor_intensity')
	flavor_notes = fields.Field(attribute='flavor_notes')
	aftertaste_score = fields.Field(attribute='aftertaste_score')
	aftertaste_notes = fields.Field(attribute='aftertaste_notes')
	acidity_score = fields.Field(attribute='acidity_score')
	acidity_intensity = fields.Field(attribute='acidity_intensity')
	acidity_notes = fields.Field(attribute='acidity_notes')
	body_score = fields.Field(attribute='body_score')
	body_intensity = fields.Field(attribute='body_intensity')
	body_notes = fields.Field(attribute='body_notes')
	balance_score = fields.Field(attribute='balance_score')
	uniformity_score = fields.Field(attribute='uniformity_score')
	cleancup_score = fields.Field(attribute='cleancup_score')
	overal_cup = fields.Field(attribute='overal_cup')
	defect = fields.Field(attribute='defect')
	cup_score = fields.Field(attribute='cup_score')


class BeansCodeAdmin(ExportActionMixin, admin.ModelAdmin):


	list_display= (


	'code',
	'beans_name',
	'jenis_kopi',
	'variety',
	'origin',
	'paska_panen',
	'vendor_name',
	'stock_terupdate',
	'nilai_stock'

		)

	list_filter= (


	'code',
	'beans_name',
	'jenis_kopi',
	'variety',
	'origin',
	'paska_panen',
	'vendor_name'

	)

	resource_class = BeansCodeResource


class BeansGudangAdmin(ExportActionMixin, admin.ModelAdmin):


	list_display = (

		'sample_code',
		'beans_name',
		'stock_status',
		'vendor_name',
		'lot_number',
		'qc_check',
		'bag',
		'inherited_stock','UOM',
		'initial_stock','UOM',
		'stock_update','UOM',
		'beans_usage_amount',
		'beans_usage_percent',
		'beans_usage_value',
		
		'roasted',
		'depreciation_average',


		'last_update'
		)

	list_filter=(
		('lot_number',PastDateRangeFilter),
		'beans_name',
		'sample_code',
		# 'stock_status',
		'vendor_name',
		('lot_number',PastDateRangeFilter),
		'qc_check',
		
		
		)

	resource_class = BeansGudangResource


class PengambilanGreenbeanAdmin(ExportActionMixin, admin.ModelAdmin):


	list_display =(
	'tanggal',
	'beans_name',
	'jumlah_diambil',
	'UOM',
	'mesin',
	'shifts',
	'pic',
	'keterangan'
)
	list_filter =(
	
	('tanggal',PastDateRangeFilter),
	('beans_name', RelatedDropdownFilter),
	'jumlah_diambil',
	'mesin',
	'shifts',
	'pic',
	'keterangan'
)

	resource_class = PengambilanGreenbeanResource
	

class RoasterAdmin(ExportActionMixin, admin.ModelAdmin):



	list_display = ('roast_date',
	'beans_name',
	'blend_name',
	'mesin',
	'profile_name',
	'shift',
	'roaster',
	'batch_number',
	'roastcode',
	'moisture_content',
	'raw',
	'UOM',
	'roasted',
	'UOM',
	'persentase_susut',
	'roaster_pass_check',
	'auto_weight_check',
	'catatan_roaster',
	'umur_roastbean')

	list_filter=(('roast_date', PastDateRangeFilter),'mesin','shift','roaster_pass_check', ('beans_name', RelatedDropdownFilter))
	# prepopulated_fields = {'susut':('persentase_susut')}

	resource_class = RoasterResource


	def changelist_view(self, request, extra_context=None):

		roasted_daily = []
		qs = Roaster.objects.all()
		froco15 = qs.filter(roast_date = today).filter(mesin= 'froco-15').aggregate(Sum('roasted'))
		froco25 = qs.filter(roast_date = today).filter(mesin= 'froco-25').aggregate(Sum('roasted'))
		context = {
		'froco15' : froco15,
		'froco25' : froco25,
		}
		return super().changelist_view(request, extra_context=context)


class BlendNameAdmin(ExportActionMixin, admin.ModelAdmin):


	list_display = ('blend_name',)
	list_filter = ('blend_name', )


class RoasterNameAdmin(ExportActionMixin, admin.ModelAdmin):


	list_display = ('roaster_technician',
		'created_date', 
		'telp',
		'address'
		)

class ProfileRoastAdmin(ExportActionMixin, admin.ModelAdmin):



	list_display = ('created_date',
		'profile_name',
		'mesin',
		'beans_name',
		'weight_lose_min',
		'weight_lose_max')
	list_filter = ('profile_name', 'beans_name')


class RoastErrorLogsAdmin(ExportActionMixin, admin.ModelAdmin):



	list_display = ('date_time', 
		'roastcode',
		'machine',
		'kronology',
		'resolution')
	list_filter = (('date_time', PastDateRangeFilter), 'machine')




admin.site.register(BeansCode, BeansCodeAdmin)
admin.site.register(BeansGudang, BeansGudangAdmin)
admin.site.register(Roaster, RoasterAdmin)
admin.site.register(PengambilanGreenbean, PengambilanGreenbeanAdmin)
admin.site.register(BlendName, BlendNameAdmin)
admin.site.register(RoasterName, RoasterNameAdmin)
admin.site.register(ProfileRoast, ProfileRoastAdmin)
admin.site.register(RoastErrorLogs, RoastErrorLogsAdmin)

