from django.db import models
#trying to one line from roastery
from products.models import Roaster
from products.models import BlendName as ProductBlendName
from django.db.models import Q
from django.utils.html import format_html, format_html_join

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

	def jumlah_input(self):
		jumlah_input = ProductionDiv.objects.filter(komposisi=self)
		return(len(jumlah_input))

	def __str__(self):
		return self.komposisi_blend
	jumlah_data = property(jumlah_input)


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
		forecast = float(self.stock_forecast_pack) + 0.001
		real = float(self.stock_masuk_pack) + 0.001
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
	blend_name_bulanan = models.ForeignKey(ProductBlendName, on_delete= models.PROTECT, limit_choices_to ={'show_this' : True}, default=1)
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
		return round(pack_forecast,2)

	def agtron_average(self):
		agtron_val = ProductionDiv.objects.filter(production_date=self)
		agtron_avg = 0
		for agtron in agtron_val:
			agtron_avg += agtron.agtron_meter
		value = float(agtron_avg) / (len(agtron_val)+0.0001)
		return round(value, 2)

	def blend_code(self):
		return "{0}/{1}/{2}/{3}/{4}".format(self.blend_name,self.machine,self.shift,self.pack_size,self.production_date)

	def readable_blend(self):
		return ('{0} [{1}]'.format(self.production_date, self.blend_name_bulanan))

	total_weight = property(total_weight)
	blend_recorded = property(count_input)
	perkiraan_jumlah_pack = property(packed_form_forcast)
	blend_id = property(blend_code)
	agtron_avg = property(agtron_average)
	readable_blend = property (readable_blend)

	def __str__(self):
		return str(self.readable_blend)




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

	kg = ('kg')
	mesin = (('fr15','fr15'), ('fr25','fr25'))
	masuk= (('Pagi','Pagi'),('Siang', 'Siang'))
	production_date= models.ForeignKey(BlendReport, on_delete=models.CASCADE, limit_choices_to={'production_date': date}  )
	roast_date = models.DateField(default=date)
	nomor_set = models.PositiveIntegerField(max_length=50,)
	roasted_material = models.ManyToManyField(Roaster, limit_choices_to = Q(next_process=False))
	komposisi = models.ForeignKey(KomposisiBean, on_delete=models.CASCADE,)
	mesin = MultiSelectField(choices=mesin)
	# shift = models.CharField(max_length=60, choices=masuk, default='')
	pack_size = models.ForeignKey(Pack, null=True, blank=True, on_delete=models.PROTECT)
	weight = models.DecimalField(max_digits=5, decimal_places=2)	
	agtron_meter = models.DecimalField(max_digits=4, decimal_places=2)
	production_process = models.BooleanField(default=True)
	production_check_pass = models.BooleanField(default=False)
	cupping = models.BooleanField(default=False)
	qc_check_pass= models.BooleanField(default=False)
	taste_notes = models.CharField(max_length=100, default='-')
	catatan_produksi = models.CharField(max_length=100, default = '-')
	catatan_qc = models.CharField(max_length=100, default='-')
	pack_status = models.BooleanField(default=False)	
	initial_create = models.DateTimeField(auto_now_add=True)

	def prepopulated_line(self):
		return "{0}{1}{2}//-set-({3})".format(self.mesin,self.production_date, self.production_date.blend_name, self.nomor_set)

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
			sekarang = datetimex
			return (sekarang), "already pack"
		elif self.cupping ==False:
			return "item need to be on cup"
		elif self.qc_check_pass == False:
			return "this  item need resolution soon"
		elif self. production_check_pass ==False:
			return "this item need resolution soon"
		else:
			return "this item still waiting to be done"

	def roasted_material_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx(self):
		qs = self.roasted_material.all()
		readable_list =[]

		for roasted in qs:
			gen = roasted.product_name
			readable_list.append([gen])
		return format_html_join('\n', "<li value = '1'>{}</li>",
			readable_list)

	def roasted_batch(self):
		qs = self.roasted_material.all()
		readable_list =[]

		for roasted in qs:
			gen = roasted.roaster_batch_name
			readable_list.append([gen])
		return format_html_join('\n', "<li>{}</li>",
			readable_list)

	def roasted_roastcode(self):
		qs = self.roasted_material.all()
		readable_list =[]

		for roasted in qs:
			gen = roasted.roaster_roastcode_name
			readable_list.append([gen])
		return format_html_join('\n', "<li>{}</li>",
			readable_list)

	def roasted_catatan(self):
		qs = self.roasted_material.all()
		readable_list =[]
		for roasted in qs:
			gen = roasted.roaster_catatan_name
			readable_list.append([gen])
		return format_html_join('\n', "<li>{}</li>",
			readable_list)

	def roasted_shift(self):
		qs = self.roasted_material.all()
		readable_list =[]
		for roasted in qs:
			gen = roasted.roaster_shift_name
			readable_list.append([gen])
		return format_html_join('\n', "<li>{}</li>",
			readable_list)

	def weight_from_roaster (self):
		qs = self.roasted_material.all()
		total_weight = 0
		for roasted in qs:
			total_weight += roasted.roasted
		return total_weight

	def hide_roaster_item(self) :
		parent_id = self.roasted_material.all()
		id_num = []
		for parent in parent_id:
			id_num.append(parent.id)
		return id_num


	def catatan_from_blend(self):
		qs = self.production_date.catatan_laporan
		return qs






	product_code = property(prepopulated_line)
	umur_blend = property(_get_umurblend)
	last_update = property(lead_time)
	parent_id = property(hide_roaster_item)
	catatan_blend = property (catatan_from_blend)
	roasted_batch = property(roasted_batch)
	roasting_shift = property(roasted_shift)
	roasted_roastcode = property(roasted_roastcode)
	roasted_catatan = property(roasted_catatan)
	total_weight = property (weight_from_roaster)

	class Meta:
		verbose_name = 'Blend & Packing'
		verbose_name_plural = 'Blend & Packing'




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



class DisposalReport(models.Model):


	unit = 'IDR'
	kg = 'Kg'
	tanggal_BAP= models.DateField()
	author = models.CharField(max_length=20)
	diketahui_oleh = models.CharField(max_length=30)
	hard_copy_url = models.URLField(default='')
	note = models.TextField(max_length=300)

	def kg_loss(self):
		total_kg = DisposalItem.objects.filter(report_id=self)
		kg_total = 0
		for kg in total_kg:
			kg_total += kg.weight
		return "\t{:,.0f}".format(kg_total)

	def value_loss(self):
		total_value = DisposalItem.objects.filter(report_id=self)
		value = 0
		for val in total_value:
			sum_val = val.weight * val.value_per_kg
			value += sum_val
		return "\t{:,.0f}".format(value)

	weight = property(kg_loss)		
	value = property(value_loss)



class DisposalItem(models.Model):


	idr = 'IDR'
	kg = 'Kg'
	report_id = models.ForeignKey(DisposalReport, on_delete=models.PROTECT)
	# created = models.DateField(default=DisposalReport.tanggal_BAP, editable=False)
	production_date = models.DateField()
	material_name = models.CharField(max_length=50)
	weight = models.DecimalField(max_digits=6, decimal_places=2)
	value_per_kg = models.PositiveIntegerField(max_length=9, default=0)	
	note = models.TextField(max_length=300)

	def item_val_loss(self):
		value = self.weight * self.value_per_kg
		return "\t{:,.0f}".format(value)

	total_value= property(item_val_loss)




class Kejadian(models.Model):

	jenis = (('B','Biasa'), ('M','Medium'),('P','Parah'),('R','Rutinitas'))
	tanggal = models.DateTimeField()
	reporter = models.CharField(max_length=15, default='-')
	tingkat_urgensi = models.CharField(max_length=1, choices=jenis, default='B')
	kronologi = models.TextField(max_length=300)
	resolusi = models.TextField(max_length=300)

	class Meta:
		verbose_name = 'Kejadian'
		verbose_name_plural = 'Kejadian'
	
