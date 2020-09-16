from django.db import models

from django.urls import reverse
from django.utils import timezone
import datetime
from datetime import timedelta
from django.db.models import Sum
from django.db.models.signals import post_save
import numpy as np
from django.utils.html import format_html
import production



date = datetime.date.today()
monday = date - datetime.timedelta(days=date.weekday())
datetimex = datetime.datetime.now()

start_week = date - datetime.timedelta(date.weekday())
end_week = start_week + datetime.timedelta(7)

month = (('JAN', 'JANUARY'), ('FEB', 'FEBRUARY'), ('MAR', 'MARCH'), ('APR', 'APRIL'),('MAY', 'MAY'), ('JUN', 'JUNE'),
		('JUL', 'JULY'),('AUG', 'AUGUST'),('SEP', 'SEPTEMBER'),('OKT', 'OKTOBER'),
		('NOV','NOVEMBER'), ('DEC', 'DECEMBER'),)

week = (('1','1'), ('2','2'),('3','3'),('4','4'),('5','5'))

daily_blend = []


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
	show_this = models.BooleanField(default=True)
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
# new update
	fr15_weight_lose_min = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	fr15_weight_lose_max = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	fr25_weight_lose_min = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	fr25_weight_lose_max = models.DecimalField(max_digits=5, decimal_places=2, default=0)
#end new update
	inherited_stock = models.DecimalField(max_digits=5, decimal_places=3, default=0.001)
	initial_stock=models.DecimalField(max_digits=10, decimal_places=2, default=1)
	price_kilo_idr = models.DecimalField(max_digits=10, decimal_places=2, default=1)
	stock_status = models.CharField(max_length=50, default='-', db_column='stock_status', null=True, blank=True)
	stock_update = models.CharField(max_length=50, default='-', db_column='stock_update',null=True, blank=True)
	roasted = models.CharField(max_length=50, default='-', db_column='roasted', null=True, blank=True)
	beans_usage_amount = models.CharField(max_length=50, default='-', db_column='beans_usage_amount', null=True, blank=True)
	beans_usage_value = models.CharField(max_length=50, default='-', db_column='beans_usage_value', null=True, blank=True)
	beans_usage_percent = models.CharField(max_length=50, default='-', db_column='beans_usage_percent', null=True, blank=True)
	# last_update_stock = models.DateTimeField(default=datetime.datetime.now)
	# stock_update = models.DecimalField(max_digits=11, decimal_places=2, default=0)
	qc_check = models.BooleanField(default=False)
	moisture_check = models.DecimalField(max_digits= 5, decimal_places= 2, default=0) # revision to decimal
	# density_check = models.CharField(max_length=30, default= 10) # add density check
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
	sweetness_score = models.DecimalField(max_digits= 5, decimal_places=2, default=0) #add sweetness score
	cleancup_score = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	overal_cup = models.DecimalField(max_digits=10, decimal_places=3, default=0)
	taint_cups = models.PositiveIntegerField(default=0, help_text= 'cup x 2')
	fault_cups = models.PositiveIntegerField(default=0, help_text= 'cup x 4')
	defect = models.CharField(max_length=100, default='-')
	cup_score = models.DecimalField(max_digits=3, decimal_places=1) # delete cup score into automatically calculate
	recomendation = models.TextField(max_length=150, default='-') # add recomendation

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
		percent_val = (float(self.initial_stock)+float(self.inherited_stock))*((float(self.limit_in_percentage)+0.0001)/100)

		if float(self.stock_update) <= percent_val and self.stock_update >= 4 :
			return format_html('<span style="color: #FFA500">STOCK LIMIT</span>')

		elif self.stock_update <= 4:
			return format_html('<span style="color: #8B0000;;">STOCK EMPTY</span>')

		else:
			return format_html('<span style="color: #228B22;">STOCK AVAILABLE</span>')

	stock_availability.allow_tags = True
	
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
			average_depreciation = round((roasted.raw - roasted.roasted)/roasted.raw*100,2)
			avg_dep += average_depreciation
		value = round(float(avg_dep)/ (len(roasted_list)+0.0001),2)
		return "{0}\t%".format(value)

	def time_update(self):
		date_list = PengambilanGreenbean.objects.filter(beans_name=self)
		sekarang = datetimex
		for date in date_list:
			sekarang = date.tanggal
		return sekarang

	def stock_update_string(self):
		rounded_val = round(self.stock_update,2)
		return f'{rounded_val:,}'
		# return '{:,2f}'.format(self.stock_update)

#for next update qc
	def final_score (self):
		frag_val = self.fragrance_score
		flav_val = self.flavor_score
		aftertaste_val = self.aftertaste_score
		acidity_val = self.acidity_score
		body_val = self.body_score
		uniformity_val = self.uniformity_score
		balance_val = self.balance_score
		cleancup_val = self.cleancup_score
		sweetness_val = self.sweetness_score
		overal_val = self.overal_cup
		total_score = frag_val + flav_val 
		+ acidity_val + body_val + uniformity_val + balance_val + cleancup_val +sweetness_val + overal_val
		taint_val = self.taint_cups * 2
		fault_val = self.fault_cups * 4
		total_defect_cup = taint_val + fault_val

		total_cup_score = float(total_score) - float(total_defect_cup)
		BeansGudang.objects.filter(id = self.id).update(cup_score=total_cup_score)

		return total_cup_score


	stock_status = property(stock_availability)
	stock_update = property(stock_updated)
	stock_akhir = property(stock_update_string)
	roasted = property(stock_roasted)
	beans_usage_amount = property(stock_usage_amount)
	beans_usage_value = property(stock_value_amount)
	beans_usage_percent = property(stock_usage_percent)
	depreciation_average = property(depreciation_in_kilo)
	# final_cup_score = property(final_score)
	last_update = property(time_update)
	coffee_score = property (final_score)

	def __str__(self):
		return self.beans_name



	class Meta:
		verbose_name = 'Bahan Baku'
		verbose_name_plural = 'Bahan Baku'


class BlendName(models.Model):

	


	created_date = models.DateField(default=date)
	blend_name = models.CharField(max_length=50, default=0)
	periode = models.CharField(max_length=3, choices=month, default='JAN')
	monthly_target = models.DecimalField(max_digits=7, decimal_places=2, default=0)
	show_this = models.BooleanField(default=True)




	def get_blendname():
		return BlendName.objects.get_or_create(id=1)

	def daily_blend(self):
		roasted_blend = Roaster.objects.filter(blend_name=self)
		nama_blend = self.blend_name
		blend_weight = 0
		for roast_val in roasted_blend:
			if roast_val.roast_date == date:
				blend_weight += roast_val.roasted
		return blend_weight

# attention to this stuff
# weekly blend val

	def week_1(self):
		roasted_blend = Roaster.objects.filter(blend_name=self).filter(minggu__in='1')
		nama_blend = self.blend_name
		blend_weight = 0
		for roast_val in roasted_blend:
			blend_weight += roast_val.roasted
		return blend_weight

	def week_2(self):
		roasted_blend = Roaster.objects.filter(blend_name=self).filter(minggu__in='2')
		nama_blend = self.blend_name
		blend_weight = 0
		for roast_val in roasted_blend:
			blend_weight += roast_val.roasted
		return blend_weight

	def week_3(self):
		roasted_blend = Roaster.objects.filter(blend_name=self).filter(minggu__in='3')
		nama_blend = self.blend_name
		blend_weight = 0
		for roast_val in roasted_blend:
			blend_weight += roast_val.roasted
		return blend_weight

	def week_4(self):
		roasted_blend = Roaster.objects.filter(blend_name=self).filter(minggu__in='4')
		nama_blend = self.blend_name
		blend_weight = 0
		for roast_val in roasted_blend:
			blend_weight += roast_val.roasted
		return blend_weight

	def week_5(self):
		roasted_blend = Roaster.objects.filter(blend_name=self).filter(minggu__in='5')
		nama_blend = self.blend_name
		blend_weight = 0
		for roast_val in roasted_blend:
			blend_weight += roast_val.roasted
		return blend_weight

	def month_production(self):
		roasted_blend = Roaster.objects.filter(blend_name=self)
		blend_weight = 0
		for roast_val in roasted_blend:
			blend_weight += roast_val.roasted
		return blend_weight

	def latest_to_target(self):
		val = self.latest - self.monthly_target 
		return val




			


	# def updated_stock (self):




	daily_updated = property (daily_blend)
	week_1 = property (week_1)
	week_2 = property (week_2)
	week_3 = property (week_3)
	week_4 = property (week_4)
	week_5 = property (week_5)
	deficiency = property (latest_to_target)
	latest = property (month_production)
	


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

#DELETED PROFILE NAME

class Roaster(models.Model):


	UOM= 'kg'
	machine = (('froco-15', 'froco-15'), ('froco-25', 'froco-25'))
	post_harvest = (('dry', 'dry'),('wet','wet'))
	nama_biji = (('cianjur','cianjur'),('ciwidey','ciwidey'))
	warna_biji = (('wajar','wajar'), ('tidak wajar', 'tidak wajar'))
	masuk= (('Pagi','Pagi'),('Siang', 'Siang'))
	roast_date = models.DateField(auto_now_add=True)
	beans_name = models.ForeignKey(BeansGudang, on_delete=models.CASCADE)
	minggu = models.CharField(max_length=1, choices=week, default='1')
	roastcode = models.CharField(max_length=20, default='-')
	blend_name = models.ForeignKey(BlendName, on_delete=models.PROTECT, default=1, limit_choices_to = {'show_this' : True}) #limit choices
	#delete profile name foreign key
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
	next_process = models.BooleanField(default=True)

	def get_absolute_url(self):
		return reverse("products:product-detail", kwargs= {'id': self.id})

	def _get_depreciation(self):
		value = round((self.raw - self.roasted)/self.raw*100 ,2)
		return "{0}\t %".format(value)

	def _get_roastage(self):
		return(date-self.roast_date)

# weight lose embeded to beansgudang
	def machine_weight_loss(self):
		weight_end = self.roasted

		if self.mesin == 'froco-15':
			min_loss_15 = self.beans_name.fr15_weight_lose_min
			max_loss_15 = self.beans_name.fr15_weight_lose_max

			if weight_end >= min_loss_15 and weight_end <= max_loss_15:
				return True
			else:
				return False

		elif self.mesin == 'froco-25':
			min_loss_25 = self.beans_name.fr25_weight_lose_min
			max_loss_25 = self.beans_name.fr25_weight_lose_max

			if weight_end >= min_loss_25 and weight_end <= max_loss_25:
				return True
			else:
				return False

	def offset_end_celcius(self):

		min_loss_15 = self.beans_name.fr15_weight_lose_min
		max_loss_15 = self.beans_name.fr15_weight_lose_max
		min_loss_25 = self.beans_name.fr25_weight_lose_min
		max_loss_25 = self.beans_name.fr25_weight_lose_max
		
		if self.mesin == 'froco-15':
			if self.roasted < min_loss_15:
				deviasi = min_loss_15 - self.roasted
			elif self.roasted > min_loss_15:
				deviasi = self.roasted - max_loss_15
			return 'Min : {0} kg - max : {1} kg  - defiasi : {2} kg'.format(min_loss_15, max_loss_15, deviasi)

		else:
			if self.roasted < min_loss_25:
				deviasi = min_loss_15 - self.roasted
			elif self.roasted > min_loss_25:
				deviasi = self.roasted - max_loss_15
			return 'Min : {0} kg - max : {1} kg  - defiasi : {2} kg'.format(min_loss_25, max_loss_25, deviasi)

	def roaster_product_name(self):
		return ('{0} {1}').format(self.beans_name, self.mesin)

	def roaster_shift(self):
		return ('{0}-{1}').format(self.shift, self.roaster)

	def roaster_batch_number(self):
		return ('{0}').format(self.batch_number,)

	def roaster_roastcode_num(self):
		return ('{0}').format(self.roastcode,)

	def roaster_mesin(self):
		return ('{0}'.format(self.mesin))

	def roaster_catatan_roaster(self):
		return ('{0}').format(self.catatan_roaster)




	def change_status(self):
		qs = production.models.ProductionDiv.objects.filter(roasted_material = self)
		self_id = self.id
		print(qs)
		already_inprocess = self.next_process
		for q in qs:

			if q.production_process == True:
			# self.next_process == True
				self.next_process = True
				Roaster.objects.filter(id = self_id).update(next_process=True)
			elif q.production_process != exist(): 
				Roaster.objects.filter(id = self_id).update(next_process=False)
				self.next_process = False
				
		return(self.next_process)

	def __str__(self):
		return self.product_name


	machine_weight_loss.boolean=True
	persentase_susut = property (_get_depreciation)
	umur_roastbean = property(_get_roastage)
	auto_control_weight = property(machine_weight_loss)
	product_name = property (roaster_product_name)
	roaster_batch_name = property(roaster_batch_number)
	roaster_roastcode_name = property(roaster_roastcode_num)
	roaster_mesin_name = property(roaster_mesin)
	roaster_catatan_name = property(roaster_catatan_roaster)
	roaster_shift_name = property(roaster_shift)
	weight_parameters = property (offset_end_celcius)

	ganti_status = property (change_status)
	
	# def __str__(self):
	# 	return self.beans_name



class PengambilanGreenbean(models.Model):

	#blend_names_embeded to pengambilan_greenbean


	UOM = 'kg'
	machine = (('froco-15', 'froco-15'), ('froco-25', 'froco-25'),('non-machine','non-machine'))
	masuk= (('Pagi','Pagi'),('Siang', 'Siang'))
	tanggal = models.DateTimeField()
	beans_name = models.ForeignKey(BeansGudang, on_delete=models.CASCADE, limit_choices_to = {'show_this' : True})
	blend_name = models.ForeignKey(BlendName, on_delete=models.PROTECT, default=1, limit_choices_to = {'show_this' : True})
	minggu = models.CharField(max_length=1, choices=week, default='1')
	jumlah_diambil = models.DecimalField(max_digits=10, decimal_places=2)
	mesin = models.CharField(max_length=50, choices=machine, default='-')
	shifts = models.CharField(max_length=50, choices=masuk, default='-')
	pic = models.CharField(max_length=50, default='-')
	keterangan = models.CharField(max_length=100, default='-')

	#add method untuk value rupiah per pengambilan 

	def value_pengambilan (self):
		qs = self.beans_name.price_kilo_idr 
		pengambilan_val = round(self.jumlah_diambil * qs,2)
		return pengambilan_val
		

	def rupiah_perpengambilan(self):
		jumlah_rupiah = self.val_gb
		return f'Rp {jumlah_rupiah:,}'

	val_gb =property(value_pengambilan)
	GB_value = property(rupiah_perpengambilan)


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


# start new def
# adding forecast and finance section

class FinancialForecast(models.Model):


	created_date = models.DateField()
	periode_bulan = models.CharField(max_length=30, default='-', help_text='Bulan disertai tahun huruf kapital eg; JANUARY 2020')
	work_days = models.PositiveIntegerField(default=1)
	catatan = models.TextField(max_length=300, default= '-')

	def val_overhead(self):
		overhead_item = OverheadItemForecast.objects.filter(parent_id = self)
		overhead_val = 0
		for cost in overhead_item:
			sum_val = cost.harga_item*cost.jumlah_item
			overhead_val += sum_val
		return overhead_val

#function to know daily forcasting daily

	def per_30days_OH(self):
		daily_oh = self.total_overhead_val / self.work_days






	def readable_total_overhead(self):
		return f'Rp {self.total_overhead_val:,}'



	total_overhead_val = property(val_overhead)
	total_overhead = property(readable_total_overhead)


class OverheadForecast(models.Model):
	created_date = models.DateField()
	# periode_bulan = models.ForeignKey()

class OverheadItemForecast(models.Model):

	# parent_id = models.ForeignKey(FinancialForecast, on_delete=models.PROTECT)
	created_date = models.DateField(auto_now_add=True)
	nama_item = models.CharField(max_length=50, default='-')
	harga_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	jumlah_item = models.DecimalField(max_digits=7, decimal_places= 2, default=0)
	total_pengeluaran = models.DecimalField(max_digits=11, decimal_places=2, default=0)
	catatan = models.TextField(max_length=300, default='-')


 







		

