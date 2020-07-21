from django.db import models

from django.urls import reverse
from django.utils import timezone
import datetime
from datetime import date
from django.db.models import Sum

date = datetime.now()


class QCSampleBean(models.Model):
	sample_code = models.CharField(max_length=10)
	sample_date = models.DateField()
	roasting_date = models.DateField()
	cupping_date = models.DateField(default=date)
	biji = models.CharField(max_length=50)
	jenis_kopi = models.CharField(max_length=10)
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

	recomendation = models.CharField(max_length=100, default='-')


class BeansGudang(models.Model):
	sample_code = models.CharField(max_length=10, default='-')
	biji = models.CharField(max_length=50)
	jenis_kopi = models.CharField(max_length=10)
	paska_panen = models.CharField(max_length=20, default='-')
	Crop_year = models.DateField()
	vendor_name = models.CharField(max_length=50)
	lot_number = models.DateField()
	bag_amount = models.PositiveIntegerField()
	qty_bag = models.PositiveIntegerField()
	berat_kopi_in_kg=models.CharField(max_length=10, default='-')

	def _get_weight_all_beans(self):
		return self.bag_amount * self.qty_bag,  'KG'

	berat_kopi_in_kg = property(_get_weight_all_beans)


	qc_acceptance = models.BooleanField(default=False)
	moisture_check = models.PositiveIntegerField(default=0)
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



	def __str__(self):
		return self.biji

	class Meta:
		verbose_name = 'Bahan Baku'
		verbose_name_plural = 'Bahan Baku'
	

class Roaster(models.Model):
	machine = (('froco-15', 'froco-15'), ('froco-25', 'froco-25'))
	post_harvest = (('dry', 'dry'),('wet','wet'))
	nama_biji = (('cianjur','cianjur'),('ciwidey','ciwidey'))
	
	warna_biji = (('wajar','wajar'), ('tidak wajar', 'tidak wajar'))
	masuk= (('Pagi','Pagi'),('Siang', 'Siang'))
	roast_date = models.DateField(auto_now_add=True)
	beans_name = models.ForeignKey(BeansGudang, on_delete=models.CASCADE)

	mesin = models.CharField(max_length=50, choices=machine, default='')
	shift = models.CharField(max_length=60, choices=masuk, default='')
	process = models.CharField(max_length=50, choices=post_harvest, default='')
	batch_number = models.PositiveIntegerField(max_length=50)
	beans_color = models.CharField(max_length=50, choices=warna_biji, default='')
	
	density = models.DecimalField(max_digits=19, decimal_places=3, default=0)
	moisture_content = models.DecimalField(max_digits=19, decimal_places=1, default=0, )
	berat_masuk = models.DecimalField(max_digits=19, decimal_places=2)
	berat_akhir = models.DecimalField(max_digits=19, decimal_places=2)
	
	roaster_pass_check = models.BooleanField(default=False)
	catatan_roaster = models.CharField(max_length=100, default='-')

	
	def get_absolute_url(self):
		return reverse("products:product-detail", kwargs= {'id': self.id})

	def _get_depreciation(self):
		return round((self.berat_masuk - self.berat_akhir)/self.berat_masuk*100,2), '%'

	def _get_roastage(self):
		return(date-self.roast_date)

	# def __str__(self):
	# 	return self.beans_name

	persentase_susut = property (_get_depreciation)

	umur_roastbean = property(_get_roastage)



