from django.shortcuts import render
from django.http import HttpResponseRedirect
import login.views 
from mainApp.models import *
import datetime

# Create your views here.

DAYS = {0:'monday', 1:'tuesday', 2:'wednesday', 3:'thursday', 4:'friday', 5:'saturday', 6:'sunday'}

def home(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")

	# if request.method == 'GET':
	    
	return render(request, "home.html")	

	# if request.method == 'POST':

def profile(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")

	return render(request,"profile.html")

	# if request.method == 'GET':
	# 	if request.GET.type == "student" :
	# 		record = Student.objects.get(ldap=request.session['id'])
	# 		if record : 
	# 			isEmpty = False
	# 		else:
	# 			isEmpty = True
	# 		return render(request,"studentProfile.html",{"isEmpty": isEmpty,"record": record, "ldap": request.session['id']})

	# 	elif request.GET.type == "mess" :
	# 		record = MessAuthority.objects.get(ID=request.session['id'])
	# 		if record : 
	# 			isEmpty = False
	# 		else:
	# 			isEmpty = True
	# 		return render(request,"messAuthorityProfile.html",{"isEmpty": isEmpty,"record": record, "ID": request.session['id']})

	# 	else :
	# 		message = "wrong type (student or mess) "
	# 		return render(request,"error.html",{"message": message})


	# elif request.method == 'POST':
	# 	if request.POST.type == "student" :
	# 		record = Student.objects.get(ldap=request.session['id'])
	# 		if record :
	# 			record.delete()
	# 		s = Student(rollNo = request.POST.rollNo, name = request.POST.name, ldap = request.POST.ldap, roomNo = request.POST.roomNo, phoneNo = request.POST.phoneNo)
	# 		s.save()

	# 	elif request.POST.type == "mess" :
	# 		record = MessAuthority.objects.get(ID=request.session['id'])
	# 		if record :
	# 			record.delete()
	# 		h  =  Hostel.objects.get(ID=request.POST.hostelID)
	# 		m = MessAuthority(ID = request.session['id'], name = request.POST.name, hostel= h , phoneNo = request.POST.phoneNo)
	# 		m.save()


# Function to display stats

def dispStats(request):

	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")

	if request.method == 'GET':
		record = Student.objects.get(ldap=request.session['id'])
		if record :
			return render(request,"dispStats.html",{"record": record})

		else:
			isEmpty = True
			return render(request,"profile.html",{"isEmpty": isEmpty,"record": record})

	elif request.method == 'POST':
		print "hi"
		# get hostel id
		# Display wastage stats in the same html


def viewMenu(request):

	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")

	if request.method == 'GET':
		return render(request,"showMenu.html")


	elif request.method == 'POST':
		if 'today' in request.POST:

			today = DAYS[datetime.datetime.today().weekday()]
			daySlot = DaySlot.objects.get(mealType__iexact=request.POST.get('mealType'), day__iexact = today)
			allHostels = Menu.objects.filter(daySlot = daySlot)
			print allHostels

		elif 'week' in request.POST:
			weeklyMenu = Menu.objects.filter(hostel_id=request.POST.get('mealType'))
			print weeklyMenu

		return render(request,"showMenu.html")



