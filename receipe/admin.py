from django.contrib import admin

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


# Register your models here.


class MaterialBucketAdmin(ExportActionMixin, admin.ModelAdmin):
	list_display = (

		 
		'material_code',
		'material_name',
		'material_price',
		'material_source',
		'material_ingredient',
		'material_legal_status',
		'expired_durability',
		'durability_notes',


		)

class MaterialUseCartAdmin(ExportActionMixin, admin.ModelAdmin):
	list_display= (

'product_parent',
'material_name',
'material_qty',
'material_uom' 

		)
	
class MaterialUseCartInline(admin.StackedInline):
	model = MaterialUseCart
	fields = (
	'product_parent',
	'material_name',
	'material_qty',
	'material_uom',
	# 'changeform_link' 
)

	# show_change_link = True

	# readonly_fields =('changeform_link',)



class MeasurementBucketAdmin(ExportActionMixin, admin.ModelAdmin):
	list_display = (

		'measurement_code',
		'measurement_notes',


		)


class ConsumerCategoryBucketAdmin(ExportActionMixin, admin.ModelAdmin):
	list_display =(
		'category_code',
		'category_name',
		'category_notes'

		)

class ProductParentCodeAdmin(ExportActionMixin, admin.ModelAdmin):
	pass

class ProductReceipeAdmin(ExportActionMixin, admin.ModelAdmin):
		inlines = [
		MaterialUseCartInline
	]
class QCSampleBeanAdmin(ExportActionMixin, admin.ModelAdmin):
	list_display =(
		'sample_code','sample_date','cupping_date','beans_name','jenis_kopi','variety','Crop_year', 'vendor_name','total_score','usage')
	list_filter=('sample_code',('sample_date', PastDateRangeFilter),'cupping_date','beans_name','jenis_kopi','Crop_year', 'vendor_name','total_score')

admin.site.register(MaterialBucket, MaterialBucketAdmin)
admin.site.register(MeasurementBucket, MeasurementBucketAdmin)
admin.site.register(ConsumerCategoryBucket, ConsumerCategoryBucketAdmin)
admin.site.register(ProductParentCode, ProductParentCodeAdmin)
admin.site.register(ProductReceipe, ProductReceipeAdmin)
admin.site.register(QCSampleBean, QCSampleBeanAdmin)
admin.site.register(MaterialUseCart, MaterialUseCartAdmin)