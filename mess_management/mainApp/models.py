from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Student(models.Model):
	rollNo = models.CharField(max_length = 20, primary_key = True)
	name = models.CharField(max_length = 50)
	ldap = models.CharField(max_length = 50)
	roomNo = models.IntegerField
	phoneNo = models.CharField(max_length = 12)

class Caterers(models.Model):
	ID = models.CharField(max_length = 20, primary_key = True)
	password = models.CharField(max_length = 50)
	name = models.CharField(max_length = 50)
	phoneno = models.CharField(max_length = 12)

class Hostels(models.Model):
	ID = models.CharField(max_length = 20, primary_key = True)
	name = models.CharField(max_length = 50)
	costPerDay = models.IntegerField

class FoodItems(models.Model):
	ID = models.CharField(max_length = 20, primary_key = True)
	name = models.CharField(max_length = 50)
	type = models.CharField(max_length = 50)
	quantity = models.CharField(max_length = 50)
	calories = models.IntegerField

class DaySlots(models.Model):
	ID = models.CharField(max_length = 20, primary_key = True)
	day  = models.CharField(max_length = 20)
	mealType  = models.CharField(max_length = 20)

class Announcement(models.Model):
	ID = models.CharField(max_length = 20, primary_key = True)
	dateTime = models.DateTimeField
	text = models.CharField(max_length = 1000)
	hostel = models.ForeignKey(Hostels, on_delete = models.CASCADE)

class MessAccounts(models.Model):
	accountNo  = models.CharField(max_length = 30, primary_key = True)
	balance = models.IntegerField
	student = models.ForeignKey(Student, on_delete = CASCADE)

class BelongsTo(models.Model):

	class Meta:
	        unique_together = (("migration", "host"),)
class Rated(models.Model):

class Reviewed(models.Model):
class Catering(models.Model):
class TempOpt(models.Model):
class Voter(models.Model):
class Extras(models.Model):
class Holidays(models.Model):
class TimeCost(models.Model):
class Quantity(models.Model):
class Menu(models.Model):





