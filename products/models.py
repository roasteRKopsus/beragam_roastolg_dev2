from django.db import models

from django.urls import reverse
from django.utils import timezone
import datetime
from django.db.models import Sum
from django.db.models.signals import post_save
import numpy as np


date = datetime.date.today()
datetimex = datetime.datetime.now()

# class BeansGudangManager(models.Manager):
# 	def stock_availability(self):
# 		if self.stock_update <= self.initial_stock/20:
# 			return "STOCK LIMIT"
# 		elif self.stock_update >= self.initial_stock/20:
# 			return "STOCK AVAILABLE"

class BeansCode(models.Model):


	code = models.CharField(max_length=10, default='-')
	beans_name = models.CharField(max_length=50)
	jenis_kopi = models.CharField(max_length=10)
	variety = models.CharField(max_length=10)
	origin = models.CharField(max_length=10)
	paska_panen = models.CharField(max_length=20, default='-')
	vendor_name = models.CharField(max_length=50)

	def kesimpulan_stock(self):
		stock_used = BeansGudang.objects.filter(sample_code=self)
		stock_updated = 0
		for stock in stock_used:
			stock_updated += stock.stock_update
		return "{0}\tKg".format(stock_updated)

	def kesimpulan_rupiah(self):
		stock_used = BeansGudang.objects.filter(sample_code=self)
		stock_rupiah = 0
		for stock in stock_used:
			update = float(stock.stock_update)
			price = float(stock.price_kilo_idr)
			value = round((update*price),2)
			stock_rupiah+=value
		return "IDR\t{:,.2f}".format(stock_rupiah)
		

	stock_terupdate = property(kesimpulan_stock)
	nilai_stock = property(kesimpulan_rupiah)

	def __str__(self):
		return self.code

	class Meta:
		verbose_name = 'GB Overview'
		verbose_name_plural = 'GB Overview'


class BeansGudang(models.Model):


	UOM= 'kg'
	sample_code = models.ForeignKey(BeansCode, on_delete=models.CASCADE)
	beans_name = models.CharField(max_length=50, help_text='format : beans name + lot_number')
	jenis_kopi = models.CharField(max_length=10)
	variety = models.CharField(max_length=10)
	origin = models.CharField(max_length=10)
	paska_panen = models.CharField(max_length=20, default='-')
	crop_year = models.DateField()
	vendor_name = models.CharField(max_length=50)
	lot_number = models.DateField()
	bag = models.PositiveIntegerField()
	qty_bag = models.PositiveIntegerField()
	limit_in_percentage = models.DecimalField(max_digits=4, decimal_places=2,default=0)
	inherited_stock = models.DecimalField(max_digits=5, decimal_places=3, default=0.001)
	initial_stock=models.DecimalField(max_digits=10, decimal_places=2, default=1)
	price_kilo_idr = models.DecimalField(max_digits=10, decimal_places=2, default=1)
	stock_status = models.CharField(max_length=50, default='-', db_column='stock_status', null=True, blank=True)
	stock_update = models.CharField(max_length=50, default='-', db_column='stock_update',null=True, blank=True)
	roasted = models.CharField(max_length=50, default='-', db_column='roasted', null=True, blank=True)
	beans_usage_amount = models.CharField(max_length=50, default='-', db_column='beans_usage_amount', null=True, blank=True)
	beans_usage_value = models.CharField(max_length=50, default='-', db_column='beans_usage_value', null=True, blank=True)
	beans_usage_percent = models.CharField(max_length=50, default='-', db_column='beans_usage_percent', null=True, blank=True)
	last_update_stock = models.DateTimeField(default=datetime.datetime.now)
	# stock_update = models.DecimalField(max_digits=11, decimal_places=2, default=0)
	qc_check = models.BooleanField(default=False)
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

	def stock_roasted(self):
		roasted_list = Roaster.objects.filter(beans_name=self)
		total_roasted = 0
		for roast in roasted_list:
			total_roasted += roast.roasted
		return total_roasted

	def stock_updated(self):
		taken_list = PengambilanGreenbean.objects.filter(beans_name=self)
		total_taken_amount = 0
		for taken in taken_list:
			total_taken_amount += taken.jumlah_diambil
		return self.inherited_stock + self.initial_stock - total_taken_amount

	def stock_availability(self):
		if self.stock_update == 0.0 < 1:
			return "EMPTY"
		elif self.stock_update < 0.2:
			return ""
		elif self.stock_update < (float(self.initial_stock)+float(self.inherited_stock))*((float(self.limit_in_percentage)+0.001)/100):
			return "LIMIT"
		elif self.stock_update > (float(self.initial_stock)+float(self.inherited_stock))*((float(self.limit_in_percentage)+0.001)/100):
			return "AVAILABLE"
	
	def stock_usage_percent(self):
		update = float(self.stock_update)
		initial = float(self.initial_stock)
		value = round((initial-update)/initial*100,2)
		return "{0}\t %".format(value)

	def stock_usage_amount(self):
		update = float(self.stock_update)
		initial = float(self.initial_stock)
		value = round((initial-update),3)
		return value

	def stock_value_amount(self):
		update = float(self.stock_update)
		initial = float(self.initial_stock)
		price = float(self.price_kilo_idr)
		value = round(((initial-update)*price),2)
		return "IDR\t{:,.2f}".format(value)

	def depreciation_in_kilo(self):
		roasted_list = Roaster.objects.filter(beans_name=self)
		avg_dep = 0
		for roasted in roasted_list:
			average_depreciation = round((roasted.raw - roasted.roasted)/roasted.roasted*100,2)
			avg_dep += average_depreciation
		value = round(float(avg_dep)/ (len(roasted_list)+0.0001),2)
		return "{0}\t%".format(value)

	def time_update(self):
		date_list = PengambilanGreenbean.objects.filter(beans_name=self)
		sekarang = datetimex
		for date in date_list:
			sekarang = date.tanggal
		return sekarang

	stock_status = property(stock_availability)
	stock_update = property(stock_updated)
	roasted = property(stock_roasted)
	beans_usage_amount = property(stock_usage_amount)
	beans_usage_value = property(stock_value_amount)
	beans_usage_percent = property(stock_usage_percent)
	depreciation_average = property(depreciation_in_kilo)
	last_update = property(time_update)

	def __str__(self):
		return self.beans_name

	class Meta:
		verbose_name = 'Bahan Baku'
		verbose_name_plural = 'Bahan Baku'


class BlendName(models.Model):


	blend_name = models.CharField(max_length=50, default=0)

	def get_blendname():
		return BlendName.objects.get_or_create(id=1)

	def __str__(self):
		return self.blend_name



class RoasterName(models.Model):


	roaster_technician = models.CharField(max_length=20)
	created_date = models.DateField()
	telp = models.PositiveIntegerField()
	address = models.CharField(max_length=50)

	def __str__(self):
		return self.roaster_technician

	def get_roastername():
		return RoasterName.objects.get_or_create(id=1)


class ProfileRoast(models.Model):


	mesin = (('froco-15', 'froco-15'), ('froco-25', 'froco-25'))
	created_date = models.DateField()
	profile_name = models.CharField(max_length=20)
	mesin = models.CharField(max_length=50, choices=mesin, default='-')
	beans_name = models.ForeignKey(BeansGudang, on_delete=models.CASCADE)
	weight_lose_min = models.DecimalField(max_digits=5,decimal_places=2, help_text='in percent')
	weight_lose_max = models.DecimalField(max_digits=5,decimal_places=2, help_text='in percent')

	def get_profileroast():
		return RoasterName.objects.get_or_create(id=1)

	def __str__(self):
		return self.profile_name


class Roaster(models.Model):


	UOM= 'kg'
	machine = (('froco-15', 'froco-15'), ('froco-25', 'froco-25'))
	post_harvest = (('dry', 'dry'),('wet','wet'))
	nama_biji = (('cianjur','cianjur'),('ciwidey','ciwidey'))
	warna_biji = (('wajar','wajar'), ('tidak wajar', 'tidak wajar'))
	masuk= (('Pagi','Pagi'),('Siang', 'Siang'))
	roast_date = models.DateField(auto_now_add=True)
	beans_name = models.ForeignKey(BeansGudang, on_delete=models.CASCADE)
	roastcode = models.CharField(max_length=20, default='-')
	blend_name = models.ForeignKey(BlendName, on_delete=models.PROTECT, default=1)
	profile_name = models.ForeignKey(ProfileRoast, on_delete=models.PROTECT, default=1)
	roaster =  models.ForeignKey(RoasterName, on_delete=models.PROTECT, default=1)
	mesin = models.CharField(max_length=50, choices=machine, default='')
	shift = models.CharField(max_length=60, choices=masuk, default='')
	process = models.CharField(max_length=50, choices=post_harvest, default='')
	batch_number = models.PositiveIntegerField(max_length=50)
	beans_color = models.CharField(max_length=50, choices=warna_biji, default='')
	density = models.DecimalField(max_digits=19, decimal_places=3, default=0)
	moisture_content = models.DecimalField(max_digits=19, decimal_places=1, default=0, )
	raw = models.DecimalField(max_digits=19, decimal_places=2)
	roasted = models.DecimalField(max_digits=19, decimal_places=2)
	roaster_pass_check = models.BooleanField(default=False)
	catatan_roaster = models.CharField(max_length=100, default='-')

	def get_absolute_url(self):
		return reverse("products:product-detail", kwargs= {'id': self.id})

	def _get_depreciation(self):
		value = round((self.raw - self.roasted)/self.raw*100 ,2)
		return "{0}\t %".format(value)

	def _get_roastage(self):
		return(date-self.roast_date)

	def auto_weight_check(self):
		weight_end = float(self.roasted)
		min_loss = float(self.profile_name.weight_lose_min)
		max_loss = float(self.profile_name.weight_lose_max)
		safe_loss = []
		for i in np.linspace(min_loss, max_loss, 0.01):
			safe_loss.append(i)
		return weight_end in safe_loss


	auto_weight_check.boolean=True
	persentase_susut = property (_get_depreciation)
	umur_roastbean = property(_get_roastage)
	auto_control_weight = property(auto_weight_check)
	
	def __str__(self):
		return self.beans_name



class PengambilanGreenbean(models.Model):


	UOM = 'kg'
	machine = (('froco-15', 'froco-15'), ('froco-25', 'froco-25'),('non-machine','non-machine'))
	masuk= (('Pagi','Pagi'),('Siang', 'Siang'))
	tanggal = models.DateTimeField()
	beans_name = models.ForeignKey(BeansGudang, on_delete=models.CASCADE)
	jumlah_diambil = models.DecimalField(max_digits=10, decimal_places=2)
	mesin = models.CharField(max_length=50, choices=machine, default='-')
	shifts = models.CharField(max_length=50, choices=masuk, default='-')
	pic = models.CharField(max_length=50, default='-')
	keterangan = models.CharField(max_length=100, default='-')

	# def save_model(self, request, obj, form, change):
	# 	obj.beans_name.stock_update - obj.jumlah_diambil
	# 	obj.beans_name.save()
	# 	super().save_model(request, obj, form, change)


class RoastErrorLogs(models.Model):


	mesin = (('froco-15', 'froco-15'), ('froco-25', 'froco-25'))
	date_time = models.DateTimeField()
	roaster = models.ForeignKey(RoasterName, on_delete=models.PROTECT, default=1)
	roastcode = models.CharField(max_length=10, default='-')
	machine = models.CharField(max_length=50, choices=mesin, default='')
	kronology = models.TextField(max_length=140, default= '-')
	resolution = models.TextField(max_length=140, default='-')



		

