# Generated by Django 3.0.8 on 2020-07-26 14:17

import datetime
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlendName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_blend', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='BlendReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('production_date', models.DateField()),
                ('catatan_laporan', models.TextField(default='-', max_length=500)),
                ('blend_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='production.BlendName')),
            ],
        ),
        migrations.CreateModel(
            name='Karyawan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_panggilan', models.CharField(max_length=20)),
                ('nama_lengkap', models.CharField(max_length=20)),
                ('no_telp', models.CharField(max_length=20)),
                ('alamat', models.CharField(max_length=100)),
                ('status_aktif', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'STAFF',
                'verbose_name_plural': 'STAFF',
            },
        ),
        migrations.CreateModel(
            name='KomposisiBean',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal_pembuatan_komposisi', models.DateField(default=datetime.date(2020, 7, 26))),
                ('kode_komposisi', models.CharField(default='-', max_length=10)),
                ('komposisi_blend', models.CharField(max_length=50)),
                ('catatan', models.CharField(default='-', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Pack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pack_name', models.CharField(max_length=20)),
                ('pack_volume', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pack_uom', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ProductionSampleBlend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_blend', models.CharField(max_length=100)),
                ('tanggal_pembuatan_sample', models.DateField(auto_now_add=True)),
                ('roast_date', models.DateField()),
                ('production_date', models.DateField()),
                ('mesin', models.CharField(choices=[('fr15', 'fr15'), ('fr25', 'fr25')], default='', max_length=50)),
                ('penerima', models.CharField(default='-', max_length=10)),
                ('diterima_qc', models.BooleanField(default=False)),
                ('catatan', models.CharField(default='-', max_length=200)),
                ('kode_sample', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='QCSampleBlend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal_diterima', models.DateField()),
                ('catatan', models.CharField(default='-', max_length=150)),
                ('qc_acceptance', models.BooleanField(default=False)),
                ('blend_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production.BlendName')),
                ('sample_blend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production.ProductionSampleBlend')),
            ],
        ),
        migrations.CreateModel(
            name='ProductionDiv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roast_date', models.DateField(default=datetime.date(2020, 7, 26))),
                ('nomor_set', models.PositiveIntegerField(max_length=50)),
                ('mesin', multiselectfield.db.fields.MultiSelectField(choices=[('fr15', 'fr15'), ('fr25', 'fr25')], max_length=9)),
                ('shift', models.CharField(choices=[('Pagi', 'Pagi'), ('Siang', 'Siang')], default='', max_length=60)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('agtron_meter', models.DecimalField(decimal_places=2, max_digits=4)),
                ('production_check_pass', models.BooleanField(default=False)),
                ('cupping', models.BooleanField(default=False)),
                ('qc_check_pass', models.BooleanField(default=False)),
                ('taste_notes', models.CharField(default='-', max_length=100)),
                ('pack_status', models.BooleanField(default=False)),
                ('initial_create', models.DateTimeField(auto_now_add=True)),
                ('komposisi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production.KomposisiBean')),
                ('pack_size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='production.Pack')),
                ('production_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production.BlendReport')),
            ],
            options={
                'verbose_name': 'Blend & Packing',
                'verbose_name_plural': 'Blend & Packing',
            },
        ),
        migrations.AddField(
            model_name='blendreport',
            name='input_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='production.Karyawan'),
        ),
        migrations.AddField(
            model_name='blendreport',
            name='pack_size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='production.Pack'),
        ),
    ]
