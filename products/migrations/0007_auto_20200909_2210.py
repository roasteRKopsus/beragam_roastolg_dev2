# Generated by Django 3.0.8 on 2020-09-09 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20200909_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='beansgudang',
            name='fr15_weight_lose_max',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='beansgudang',
            name='fr15_weight_lose_min',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='beansgudang',
            name='fr25_weight_lose_max',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='beansgudang',
            name='fr25_weight_lose_min',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
