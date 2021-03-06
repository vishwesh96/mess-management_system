# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 04:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('dateTime', models.DateTimeField()),
                ('subject', models.CharField(default='Notification', max_length=50)),
                ('text', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='BelongsTo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateField()),
                ('endDate', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Caterer',
            fields=[
                ('ID', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('phoneno', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Catering',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDateTime', models.DateTimeField()),
                ('endDateTime', models.DateTimeField()),
                ('caterer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Caterer')),
            ],
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mealType', models.CharField(max_length=20)),
                ('cost', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DaySlot',
            fields=[
                ('ID', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('day', models.CharField(max_length=20)),
                ('mealType', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Deduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.IntegerField(default=0)),
                ('deduct', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Extras',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('ID', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('quantity', models.CharField(max_length=50)),
                ('calories', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Holidays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('daySlot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.DaySlot')),
            ],
        ),
        migrations.CreateModel(
            name='Hostel',
            fields=[
                ('ID', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('costPerDay', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daySlot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.DaySlot')),
                ('food', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainApp.FoodItem')),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Hostel')),
            ],
        ),
        migrations.CreateModel(
            name='MessAuthority',
            fields=[
                ('ID', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('phoneNo', models.CharField(max_length=12)),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Hostel')),
            ],
        ),
        migrations.CreateModel(
            name='Quantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantityRequired', models.IntegerField()),
                ('daySlot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.DaySlot')),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Hostel')),
            ],
        ),
        migrations.CreateModel(
            name='Rated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taste', models.IntegerField(null=True)),
                ('costEffective', models.IntegerField(null=True)),
                ('cleanliness', models.IntegerField(null=True)),
                ('overall', models.IntegerField(null=True)),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Hostel')),
            ],
        ),
        migrations.CreateModel(
            name='Reviewed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=1000)),
                ('dateTime', models.DateTimeField()),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Hostel')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('rollNo', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('ldap', models.CharField(max_length=50, unique=True)),
                ('roomNo', models.IntegerField()),
                ('phoneNo', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='TempOpt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('startMealType', models.CharField(max_length=20)),
                ('endMealType', models.CharField(max_length=20)),
                ('hostel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.Hostel')),
            ],
        ),
        migrations.CreateModel(
            name='Wastage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField()),
                ('wasted', models.DecimalField(decimal_places=2, max_digits=4)),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Hostel')),
            ],
        ),
        migrations.CreateModel(
            name='MessAccounts',
            fields=[
                ('accountNo', models.CharField(max_length=30)),
                ('balance', models.IntegerField(default=0)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mainApp.Student')),
            ],
        ),
        migrations.AddField(
            model_name='tempopt',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Student'),
        ),
        migrations.AddField(
            model_name='reviewed',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainApp.Student'),
        ),
        migrations.AddField(
            model_name='rated',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainApp.Student'),
        ),
        migrations.AddField(
            model_name='holidays',
            name='hostel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Hostel'),
        ),
        migrations.AddField(
            model_name='extras',
            name='food',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.FoodItem'),
        ),
        migrations.AddField(
            model_name='extras',
            name='hostel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Hostel'),
        ),
        migrations.AddField(
            model_name='deduct',
            name='hostel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Hostel'),
        ),
        migrations.AddField(
            model_name='cost',
            name='hostel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Hostel'),
        ),
        migrations.AddField(
            model_name='catering',
            name='hostel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Hostel'),
        ),
        migrations.AddField(
            model_name='belongsto',
            name='hostel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Hostel'),
        ),
        migrations.AddField(
            model_name='belongsto',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Student'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='hostel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Hostel'),
        ),
        migrations.AlterUniqueTogether(
            name='wastage',
            unique_together=set([('hostel', 'day')]),
        ),
        migrations.AlterUniqueTogether(
            name='tempopt',
            unique_together=set([('student', 'hostel', 'startDate', 'startMealType')]),
        ),
        migrations.AlterUniqueTogether(
            name='reviewed',
            unique_together=set([('student', 'hostel', 'dateTime')]),
        ),
        migrations.AlterUniqueTogether(
            name='rated',
            unique_together=set([('student', 'hostel')]),
        ),
        migrations.AlterUniqueTogether(
            name='quantity',
            unique_together=set([('hostel', 'daySlot')]),
        ),
        migrations.AlterUniqueTogether(
            name='menu',
            unique_together=set([('daySlot', 'hostel', 'food')]),
        ),
        migrations.AlterUniqueTogether(
            name='holidays',
            unique_together=set([('hostel', 'daySlot', 'date')]),
        ),
        migrations.AlterUniqueTogether(
            name='extras',
            unique_together=set([('hostel', 'food')]),
        ),
        migrations.AlterUniqueTogether(
            name='cost',
            unique_together=set([('hostel', 'mealType')]),
        ),
        migrations.AlterUniqueTogether(
            name='catering',
            unique_together=set([('caterer', 'hostel', 'startDateTime')]),
        ),
        migrations.AlterUniqueTogether(
            name='belongsto',
            unique_together=set([('student', 'startDate')]),
        ),
    ]
