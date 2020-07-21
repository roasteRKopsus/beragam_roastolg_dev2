from django.db import models

from multiselectfield import MultiSelectField
import datetime

date = datetime.date.today()

class KomposisiBean(models.Model):
	tanggal_pembuatan_komposisi = models.DateField(default=date)
	kode_komposisi = models.CharField(max_length=10, default='-')

	komposisi_blend = models.CharField(max_length=50)
	catatan = models.CharField(max_length = 200, default='-')
	def __str__(self):
		return self.komposisi_blend
class BlendName(models.Model):
	nama_blend = models.CharField(max_length=50)
	def __str__(self):
		return self.nama_blend


# Create your models here.
class ProductionDiv(models.Model):
	nama_blend = (('kenangan_blend','kenangan_blend'),('tetangga_blend','tetangga_blend'), 
		('cipete_blend','cipete_blend'),('ciung_wanara','ciung_wanara'),('waste_coffe','waste_coffe'))
	mesin = (('froco-15','froco-15'), ('froco-25','froco-25'))
	# nama_biji = BeansName.objects.all()
	# jenis_beans = BeansName.objects.all()
	tanggal_blend = models.DateField()
	roast_date = models.DateField(default=date)
	nomor_set = models.PositiveIntegerField(max_length=50)
	komposisi = models.ForeignKey(KomposisiBean, on_delete=models.CASCADE)
	mesin = (MultiSelectField(choices=mesin))

	jenis_blend = models.ForeignKey(BlendName, on_delete=models.CASCADE)
	blend_code = models.CharField(max_length=50)
	weight = models.DecimalField(max_length=50, max_digits=5, decimal_places=2)
	
	agtron_meter = models.PositiveIntegerField(max_length=50, default=0)
	production_check_pass = models.BooleanField(default=False)
	cupping = models.BooleanField(default=False)
	
	qc_check_pass= models.BooleanField(default=False)
	taste_notes = models.CharField(max_length=100, default='-')
	pack_status = models.BooleanField(default=False)
	product_code = models.SlugField(allow_unicode=True)

	



	def get_absolute_url(self):
		return reverse("production:production-detail", kwargs= {'id': self.id})

	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in ProductionDiv._meta.fields]

	def _get_umurblend(self):
		return(date-self.tanggal_blend)



	umur_blend = property(_get_umurblend)



	class Meta:
		verbose_name = 'blending section'


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
