# Generated by Django 3.0.8 on 2020-08-24 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20200808_0233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beansgudang',
            name='inherited_stock',
            field=models.DecimalField(decimal_places=3, default=0.001, max_digits=5),
        ),
    ]
