# Generated by Django 3.0.8 on 2020-09-17 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_17sep20'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roaster',
            name='set_number',
            field=models.PositiveIntegerField(max_length=5),
        ),
    ]
#DONE UPDATED 17 sep 20