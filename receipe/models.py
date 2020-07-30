from django.db import models

from django.urls import reverse
from django.utils import timezone
import datetime
from django.db.models import Sum
from django.db.models.signals import post_save

date = datetime.date.today()
# Create your models here.

	

class MeasurementBucket(models.Model):
	measurement_code = models.CharField(max_length=100)
	measurement_notes = models.CharField(max_length=100)
	
	def __str__(self):
		return self.measurement_code

class ConsumerCategoryBucket(models.Model):
	category_code = models.CharField(max_length=100)
	category_name = models.CharField(max_length=100)
	category_notes = models.CharField(max_length=500)
	
	def __str__(self):
		return self.category_name

class ProductParentCode(models.Model):
	parents_code = models.CharField(max_length=20)
	code_issued_date = models.DateField()
	code_notes = models.CharField(max_length=300)
	
	def __str__(self):
		return self.parents_code

class ProductReceipe(models.Model):
	created = models.DateField(default=date)
	market_category = models.ForeignKey(ConsumerCategoryBucket, on_delete=models.CASCADE)
	product_parents = models.ForeignKey(ProductParentCode, on_delete=models.CASCADE)
	product_name = models.CharField(max_length=100)
	product_code = models.CharField(max_length=100)
	issued_by = models.CharField(max_length=100)
	procedure = models.TextField(max_length=3000)
	notes = models.TextField(max_length=3000)



	def __str__(self):
		return self.product_code



class MaterialBucket(models.Model):
	durability =(('very short less than day','very short lest than day'),('short less than week','short less than week'),
		('medium less than 3 month','short less than 3 month'), 
		('long more than 3 month','long more than 3 month')) 
	material_code = models.CharField(max_length=50, default='-')
	material_name = models.CharField( max_length=50, default='-')
	material_price = models.DecimalField(max_digits=10,null=True,blank=True, decimal_places=2)
	material_source = models.CharField(max_length=100, default='-')
	material_ingredient = models.CharField(max_length=200, default='-')
	material_legal_status = models.CharField(max_length=200, default='-')
	expired_durability = models.CharField(max_length=100, choices=durability)
	durability_notes = models.CharField(max_length=300)
	
	def __str__(self):
		return self.material_name

class MaterialUseCart(models.Model):
	product_parent =  models.ForeignKey(ProductReceipe, on_delete=models.CASCADE)
	material_name = models.ForeignKey(MaterialBucket, on_delete=models.CASCADE)
	material_qty = models.DecimalField(max_digits=10,null=True,blank=True, decimal_places=2)
	material_uom = models.ForeignKey(MeasurementBucket, on_delete=models.CASCADE)



	# def changeform_link(self):
	# 	if self.id:
	# 		changeform_url = urlresolvers.reverse(
	# 			'admin:receipe_productreceipe_change', args=(self.id,)
	# 			)
	# 		return u'<a href="%s" target="_blank">Details</a>' % changeform_url
	# 	return u''
	# changeform_link.allow_tags = True
	# changeform_link.short_description = ''


	

class QCSampleBean(models.Model):
	best_option = (('e','espresso'),('m','manual brew'), ('b','espresso & manual'),('n','nothing'))
	sample_code = models.CharField(max_length=10)
	sample_date = models.DateField()
	roasting_date = models.DateField()
	cupping_date = models.DateField(default=date)
	beans_name = models.CharField(max_length=10)
	jenis_kopi = models.CharField(max_length=10)
	variety = models.CharField(max_length=10)
	origin = models.CharField(max_length=10)
	paska_panen = models.CharField(max_length=20, default='-')
	Crop_year = models.DateField()
	vendor_name = models.CharField(max_length=50)	
	qc_acceptance = models.BooleanField(default=False)
	moisture_check = models.DecimalField(default=0, max_digits=10, decimal_places=3)
	primary_defect = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	secondary_defect = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	aroma_greenbean = models.CharField(max_length=100, default='-')
	fragrance_score = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	fragrance_intensity = models.CharField(max_length=100, default='-')
	fragrance_notes = models.CharField(max_length=100, default='-')
	flavor_score = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	flavor_intensity = models.CharField(max_length=100, default='-')
	flavor_notes = models.CharField(max_length=100, default='-')
	aftertaste_score = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	aftertaste_notes = models.CharField(max_length=100, default='-')
	acidity_score = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	acidity_intensity = models.CharField(max_length=100, default='-')
	acidity_notes = models.CharField(max_length=100, default='-')
	body_score = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	body_intensity = models.CharField(max_length=100, default='-')
	body_notes = models.CharField(max_length=100, default='-')
	balance_score = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	uniformity_score = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	cleancup_score = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	overal_cup = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	defect = models.CharField(max_length=100, default='-')
	cup_score = models.DecimalField(max_digits=3, decimal_places=1)
	total_score = models.DecimalField(max_digits=3, decimal_places=1)
	usage = models.CharField(max_length=1, choices=best_option, default='n')
	recomendation = models.TextField(max_length=100, default='-')


	class Meta:
		verbose_name = 'Coffee Research'
		verbose_name_plural = 'Coffee Research'




	