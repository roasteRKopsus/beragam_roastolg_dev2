from django.db import models

from multiselectfield import MultiSelectField
from datetime import datetime, timezone, date


datetimex = datetime.now(timezone.utc)

date = date.today()
STATUS_NOW = [('p','pending'),('c','confirmed')]

class KomposisiBean(models.Model):
	tanggal_pembuatan_komposisi = models.DateField(default=date)
	kode_komposisi = models.CharField(max_length=10, default='-')

	komposisi_blend = models.CharField(max_length=50)
	catatan = models.CharField(max_length = 200, default='-')
	def __str__(self):
		return self.komposisi_blend

class DaftarCustomer(models.Model):

	nama_customer = models.CharField(max_length=20)
	no_telp = models.CharField(max_length=20)
	alamat = models.CharField(max_length=30)
	pic = models.CharField(max_length=30)

	def jumlah_pemesanan_volume(self):
		sum_order = BarangKeluar.objects.filter(customer=self)
		total_order = 0
		for order in sum_order:
			total_order += order.volume_quantity
		return total_order

	total_weight = property(jumlah_pemesanan_volume)

	def __str__(self):
		return self.nama_customer


	
class Pack(models.Model):
	pack_name = models.CharField(max_length=20)
	pack_volume = models.DecimalField(max_digits=9, decimal_places=2)
	pack_uom = models.CharField(max_length=20)

	def __str__(self):
		return self.pack_name


class Karyawan(models.Model):
	nama_panggilan = models.CharField(max_length=20)
	nama_lengkap = models.CharField(max_length=20)
	no_telp = models.CharField(max_length=20)
	alamat = models.CharField(max_length=100)
	status_aktif = models.BooleanField(default=False)

	def __str__(self):
		return self.nama_panggilan

	class Meta:
		verbose_name = 'STAFF'
		verbose_name_plural = 'STAFF'



class BlendName(models.Model):
	nama_blend = models.CharField(max_length=50)

	def __str__(self):
		return self.nama_blend




class RunTimeStock(models.Model):
	kg = 'Kg'
	pcs = 'Pcs'
	blend_name = models.ForeignKey(BlendName, on_delete=models.PROTECT)
	pack_size = models.ForeignKey(Pack, on_delete=models.PROTECT)

	def stock_runtime_pack (self):
		stock_input = PackFormInput.objects.filter(blend_name=self)
		stock_output = BarangKeluar.objects.filter(blend_name=self)
		stock_entry = 0
		for stock in stock_input:
			stock_entry += stock.volume_pack
		for stock in stock_output:
			stock_entry -= stock.volume_pack
		return stock_entry

	def stock_runtime_qty (self):
		stock_input = PackFormInput.objects.filter(blend_name=self)
		stock_output = BarangKeluar.objects.filter(blend_name=self)
		stock_entry = 0
		for stock in stock_input:
			stock_entry += stock.volume_quantity
		for stock in stock_output:
			stock_entry -= stock.volume_quantity
		return stock_entry

	def stock_in_pack(self):
		stock_input = PackFormInput.objects.filter(blend_name=self)
		stock_in = 0
		for stock in stock_input:
			stock_in += stock.volume_pack
		return stock_in


	def stock_in_qty(self):
		stock_input = PackFormInput.objects.filter(blend_name=self)
		stock_in = 0
		for stock in stock_input:
			stock_in += stock.volume_quantity
		return stock_in

	def stock_out_pack(self):
		stock_input = BarangKeluar.objects.filter(blend_name=self)
		stock_in = 0
		for stock in stock_input:
			stock_in += stock.volume_pack
		return '{0}\tPcs'.format(stock_in)

	def stock_out_qty(self):
		stock_input = BarangKeluar.objects.filter(blend_name=self)
		stock_in = 0
		for stock in stock_input:
			stock_in += stock.volume_quantity
		return '{0}\tKg'.format(stock_in)

	def stock_forecast_pack(self):
		stock_input = BlendReport.objects.filter(blend_name=self)
		stock_in = 0
		for stock in stock_input:
			stock_in += stock.perkiraan_jumlah_pack
		return stock_in
	def stock_forecast_qty(self):
		stock_input = BlendReport.objects.filter(blend_name=self)
		stock_in = 0
		for stock in stock_input:
			stock_in += stock.total_weight
		return stock_in

	def margin_forecast_to_real_kg(self):
		forecast = self.stock_forecast_qty
		real = self.stock_masuk_qty
		value = real - forecast
		return '{0}\tKg'.format(value)

	def margin_forecast_to_real_pcs(self):
		forecast = self.stock_forecast_pack
		real = self.stock_masuk_pack
		value = real - forecast
		return '{0}\tpcs'.format(value)

	def margin_forecast_to_real_percent(self):
		forecast = self.stock_forecast_pack + 0.001
		real = self.stock_masuk_pack + 0.001
		value = round((forecast-real)/forecast*100,2)
		return '{0}\t%'.format(value)


	stock_forecast_pack = property(stock_forecast_pack)
	stock_forecast_qty = property(stock_forecast_qty)
	stock_masuk_pack = property(stock_in_pack)
	stock_masuk_qty = property(stock_in_qty)
	forecast_vs_real_kg = property(margin_forecast_to_real_kg)
	forecast_vs_real_pcs = property(margin_forecast_to_real_pcs)
	forecast_vs_real_percentage = property(margin_forecast_to_real_percent)


	stock_keluar_pack = property(stock_out_pack)
	stock_keluar_qty = property(stock_out_qty)
	stock_update_pack = property (stock_runtime_pack)
	stock_update_quantity = property (stock_runtime_qty)

	def __str__(self):
		return str(self.blend_name)
		


class BlendReport(models.Model):
	uom = 'kg'
	mesin = (('a', 'fr15'), ('b', 'fr25'),('c','fr15-25'))
	masuk =(('a','pagi'),('b','siang'))
	production_date = models.DateField()
	machine = MultiSelectField(choices=mesin,)
	shift = MultiSelectField(choices=masuk)
	blend_name = models.ForeignKey(RunTimeStock, on_delete=models.PROTECT)
	pack_size = models.ForeignKey(Pack, on_delete=models.PROTECT)
	input_by = models.ForeignKey(Karyawan, on_delete=models.PROTECT)
	catatan_laporan = models.TextField(max_length=500, default='-')
	

	def count_input (self):
		data_input = ProductionDiv.objects.filter(production_date=self)
		return len(data_input)

	def total_weight (self):
		sum_weight = ProductionDiv.objects.filter(production_date=self)
		initial_weight = 0
		for weight in sum_weight:
			initial_weight += weight.weight
		return initial_weight

	def packed_form_forcast(self):
		pack_vol = self.pack_size.pack_volume
		pack_forecast = self.total_weight*1000/pack_vol
		return pack_forecast

	def agtron_average(self):
		agtron_val = ProductionDiv.objects.filter(production_date=self)
		agtron_avg = 0
		for agtron in agtron_val:
			agtron_avg += agtron.agtron_meter
		value = float(agtron_avg) / (len(agtron_val)+0.0001)
		return round(value, 2)


	def blend_code(self):
		return "{0}/{1}/{2}/{3}/{4}".format(self.blend_name,self.machine,self.shift,self.pack_size,self.production_date)

	total_weight = property(total_weight)
	blend_recorded = property(count_input)
	perkiraan_jumlah_pack = property(packed_form_forcast)
	blend_id = property(blend_code)
	agtron_avg = property(agtron_average)





	def __str__(self):
		return str(self.production_date)




class PackFormInput(models.Model):
	pcs = 'Pcs'
	kg ='Kg'
	tanggal_dan_jam = models.DateTimeField(default=datetimex)
	blend_name = models.ForeignKey(RunTimeStock, on_delete=models.PROTECT)	
	jenis_pack = models.ForeignKey(Pack, on_delete=models.PROTECT)
	volume_pack = models.DecimalField(max_digits=9, decimal_places=2)
	volume_quantity = models.DecimalField(max_digits=9, decimal_places=2)
	catatan = models.TextField(max_length=200, default='-')

	def __str__(self):
		return str(self.blend_name)

	class Meta:
		verbose_name = 'Finish Good Input'
		verbose_name_plural = 'Finish Good Input'

class BarangKeluar(models.Model):
	tanggal_dan_jam = models.DateTimeField(default=datetimex)
	blend_name = models.ForeignKey(RunTimeStock, on_delete=models.PROTECT)
	invoice_number = models.CharField(max_length=20, default='-')
	customer = models.ForeignKey(DaftarCustomer, on_delete=models.PROTECT)
	jenis_pack = models.ForeignKey(Pack, on_delete=models.PROTECT)
	volume_pack = models.DecimalField(max_digits=9, decimal_places=2)
	volume_quantity = models.DecimalField(max_digits=9, decimal_places=2)
	catatan = models.TextField(max_length=200, default='-')


	def __str__(self):
		return str(self.blend_name)

	class Meta:
		verbose_name = 'Barang Keluar'
		verbose_name_plural = 'Barang Keluar'

class ProductionDiv(models.Model):

	mesin = (('fr15','fr15'), ('fr25','fr25'))
	masuk= (('Pagi','Pagi'),('Siang', 'Siang'))

	production_date= models.ForeignKey(BlendReport, on_delete=models.CASCADE)
	roast_date = models.DateField(default=date)
	nomor_set = models.PositiveIntegerField(max_length=50)
	komposisi = models.ForeignKey(KomposisiBean, on_delete=models.CASCADE)
	mesin = MultiSelectField(choices=mesin)
	shift = models.CharField(max_length=60, choices=masuk, default='')
	pack_size = models.ForeignKey(Pack, null=True, blank=True, on_delete=models.PROTECT)
	weight = models.DecimalField(max_digits=5, decimal_places=2)
	
	agtron_meter = models.DecimalField(max_digits=4, decimal_places=2)
	production_check_pass = models.BooleanField(default=False)
	# cupping = models.CharField(max_length=1, choices=STATUS_NOW, default='p')
	cupping = models.BooleanField(default=False)
	qc_check_pass= models.BooleanField(default=False)
	taste_notes = models.CharField(max_length=100, default='-')
	pack_status = models.BooleanField(default=False)
	
	initial_create = models.DateTimeField(auto_now_add=True)


	
	def prepopulated_line(self):
		return "{0}-{1}-{2}-{3}-set-({4})".format(self.mesin,self.shift,self.production_date, self.production_date.blend_name, self.nomor_set)

	def weight_to_pack(self):
		return self.weight/self.pack_size


	def get_absolute_url(self):
		return reverse("production:production-detail", kwargs= {'id': self.id})

	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in ProductionDiv._meta.fields]

	def _get_umurblend(self):
		return (date-self.roast_date)

	def lead_time(self):
		if self.pack_status==True:
			return (datetimex - self.initial_create), "already pack"
		elif self.cupping ==False:
			return "item need to be on cup"
		elif self.qc_check_pass == False:
			return "this  item need resolution soon"
		elif self. production_check_pass ==False:
			return "this item need resolution soon"

		else:
			return "this item still waiting to be done"
	# def lead_time (self):
	# 	if self. 


	product_code = property(prepopulated_line)
	umur_blend = property(_get_umurblend)
	last_update = property(lead_time)



	class Meta:
		verbose_name = 'Blend & Packing'
		verbose_name_plural = 'Blend & Packing'


	# def __str__(self):
	# 	return  (self.jenis_blend, self.nomor_set)

class ProductionSampleBlend(models.Model):
	machine = (('fr15', 'fr15'), ('fr25', 'fr25'))
	nama_blend =models.CharField(max_length=100)
	
	tanggal_pembuatan_sample = models.DateField(auto_now_add=True)
	roast_date = models.DateField()
	production_date= models.DateField()
	mesin = models.CharField(max_length=50, choices=machine, default='')
	penerima = models.CharField(max_length=10, default='-')
	diterima_qc= models.BooleanField(default=False)

	catatan = models.CharField(max_length=200, default='-')
	kode_sample =models.CharField(max_length=100)

	

	def __str__(self):
		return self.mesin

	def __str__(self):
		return self.kode_sample

class QCSampleBlend(models.Model):
	tanggal_diterima = models.DateField()
	blend_name = models.ForeignKey(BlendName, on_delete=models.CASCADE)
	sample_blend=models.ForeignKey(ProductionSampleBlend, on_delete=models.CASCADE)
	catatan = models.CharField(max_length=150, default='-')
	
	qc_acceptance =models.BooleanField(default=False)
