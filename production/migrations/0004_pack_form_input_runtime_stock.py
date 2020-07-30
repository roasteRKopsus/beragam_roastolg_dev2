# Generated by Django 3.0.8 on 2020-07-27 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0003_auto_20200727_1647'),
    ]

    operations = [
        migrations.CreateModel(
            name='runtime_stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blend_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='production.BlendName')),
            ],
        ),
        migrations.CreateModel(
            name='pack_form_input',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jumlah_pack', models.DecimalField(decimal_places=2, max_digits=9)),
                ('blend_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='production.BlendName')),
            ],
        ),
    ]
