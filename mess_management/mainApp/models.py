from __future__ import unicode_literals

from django.db import models

# Create your models here.

#many constraints in "unique together have been changed"
class Student(models.Model):
	rollNo = models.CharField(max_length = 20, primary_key = True)
	name = models.CharField(max_length = 50)
	ldap = models.CharField(max_length = 50, unique=True)
	roomNo = models.IntegerField()
	phoneNo = models.CharField(max_length = 12)

class Caterer(models.Model):
	ID = models.CharField(max_length = 20, primary_key = True)
	name = models.CharField(max_length = 50)
	phoneno = models.CharField(max_length = 12)
	

class Hostel(models.Model):
	ID = models.CharField(max_length = 20, primary_key = True)
	name = models.CharField(max_length = 50)
	costPerDay = models.IntegerField()
	
#added new relation
class MessAuthority(models.Model):
	ID = models.CharField(max_length = 20, primary_key = True)
	hostel = models.ForeignKey(Hostel, on_delete = models.CASCADE)
	name = models.CharField(max_length = 50)
	phoneNo = models.CharField(max_length = 12)
	
class FoodItem(models.Model):
	ID = models.CharField(max_length = 20, primary_key = True)
	name = models.CharField(max_length = 50)
	type = models.CharField(max_length = 50)
	quantity = models.CharField(max_length = 50)
	calories = models.IntegerField()

class DaySlot(models.Model):
	ID = models.CharField(max_length = 20, primary_key = True)
	day  = models.CharField(max_length = 20)
	mealType  = models.CharField(max_length = 20)

class Announcement(models.Model):
	ID = models.CharField(max_length = 20, primary_key = True)
	dateTime = models.DateTimeField()
	text = models.CharField(max_length = 1000)
	hostel = models.ForeignKey(Hostel, on_delete = models.CASCADE)

#changed fromER diagram:Roll number if primary key and the relation in one-to-one with student
class MessAccounts(models.Model):
	accountNo  = models.CharField(max_length = 30)
	balance = models.IntegerField(default=0)
	student = models.OneToOneField( 
					Student,
					on_delete=models.CASCADE,
					primary_key=True,
					)

#changed the uniqueness condition on combined attributes
class BelongsTo(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE) 
	startDate = models.DateField()
	endDate = models.DateField(null=True)
	class Meta:
		unique_together = (("student", "startDate"),)

#changed the uniqueness condition on combined attributes
class Rated(models.Model):
	student = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True) 
	hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE) 
	taste = models.IntegerField(null=True) 
	costEffective = models.IntegerField(null=True)
	cleanliness = models.IntegerField(null=True)
	overall = models.IntegerField(null=True)
	class Meta:
		unique_together = (("student","hostel"),)
	
class Reviewed(models.Model):
	student = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True) 
	hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE) 
	review = models.CharField(max_length = 1000)
	dateTime = models.DateTimeField()
	class Meta:
		unique_together = (("student","hostel","dateTime"),)	

#endDate is fixed by startDate
class Catering(models.Model):
	caterer = models.ForeignKey(Caterer, on_delete=models.CASCADE) 
	hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE) 
	startDateTime = models.DateTimeField() 
	endDateTime = models.DateTimeField()
	class Meta:
		unique_together = (("caterer","hostel","startDateTime"),)


class TempOpt(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE) 
	hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, null =True) 
	startDate = models.DateField()
	endDate = models.DateField()
	startMealType = models.CharField(max_length = 20)
	endMealType = models.CharField(max_length = 20)
	class Meta: #might have overlapping intervals, but check this constraint oin application
		#hostel value can be null and unique togther added hostel as holiday 
		unique_together = (("student","hostel","startDate","startMealType"),)

class Voter(models.Model):
	student = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True)
	food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
	class Meta:
		unique_together = (("student", "food"),)	

class Extras(models.Model):
	hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE) 
	food = models.ForeignKey(FoodItem, on_delete=models.CASCADE) 
	cost = models.IntegerField()
	class Meta:
		unique_together = (("hostel", "food"),)	

class Holidays(models.Model):
	daySlot = models.ForeignKey(DaySlot, on_delete=models.CASCADE) 
	hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE) 
	date = models.DateTimeField()
	class Meta:
		unique_together = (("hostel", "daySlot", "date"),)

class TimeCost(models.Model):
	daySlot = models.ForeignKey(DaySlot, on_delete=models.CASCADE) 
	hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE) 
	originalCost = models.IntegerField()
	subsidisedCost = models.IntegerField()
	startTime = models.DateTimeField()
	endTime = models.DateTimeField()
	class Meta:
		unique_together = (("hostel", "daySlot"),)

class Quantity(models.Model):
	daySlot = models.ForeignKey(DaySlot, on_delete=models.CASCADE) 
	hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
	quantityRequired = models.IntegerField()
	wasted = models.DecimalField(max_digits=4,decimal_places=2)
	class Meta:
		unique_together = (("hostel", "daySlot"),)

class Menu(models.Model):
	daySlot = models.ForeignKey(DaySlot, on_delete=models.CASCADE) 
	hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE) 
	food = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, blank=True, null=True) #ask??????????????? both foreign and primary how??
	class Meta:
		unique_together = (("daySlot", "hostel", "food"),)





