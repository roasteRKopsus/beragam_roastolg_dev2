# Generated by Django 3.0.8 on 2020-07-30 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_beansgudang_inherited_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='beansgudang',
            name='limit_in_percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
    ]
