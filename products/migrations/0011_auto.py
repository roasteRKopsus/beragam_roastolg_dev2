# Generated by Django 3.0.8 on 2020-09-11 20:28
#DONE UPDATE TO PRODUCTION SERVER 12 sep 2020
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blendname',
            old_name='show_status',
            new_name='show_this',
        ),
        migrations.AlterField(
            model_name='roaster',
            name='blend_name',
            field=models.ForeignKey(default=1, limit_choices_to={'show_this': True}, on_delete=django.db.models.deletion.PROTECT, to='products.BlendName'),
        ),
    ]
