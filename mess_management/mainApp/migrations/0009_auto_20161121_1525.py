# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-21 15:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0008_auto_20161103_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rated',
            name='cleanliness',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='rated',
            name='costEffective',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='rated',
            name='overall',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='rated',
            name='taste',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='reviewed',
            name='review',
            field=models.CharField(max_length=10),
        ),
    ]
