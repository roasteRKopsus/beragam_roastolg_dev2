# Generated by Django 3.0.8 on 2020-09-16 12:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_12sep20'),
    ]

    operations = [
        migrations.AddField(
            model_name='beansgudang',
            name='fault_cups',
            field=models.PositiveIntegerField(default=0, help_text='cup x 4'),
        ),
        migrations.AddField(
            model_name='beansgudang',
            name='recomendation',
            field=models.TextField(default='-', max_length=150),
        ),
        migrations.AddField(
            model_name='beansgudang',
            name='sweetness_score',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='beansgudang',
            name='taint_cups',
            field=models.PositiveIntegerField(default=0, help_text='cup x 2'),
        ),
        migrations.AlterField(
            model_name='blendname',
            name='created_date',
            field=models.DateField(default=datetime.date(2020, 9, 16)),
        ),
    ]
