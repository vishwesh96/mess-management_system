# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 13:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='ldap',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
