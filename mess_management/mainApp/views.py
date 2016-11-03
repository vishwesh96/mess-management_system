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

	if request.method == 'GET':	
		print request.GET.get('type')
		if request.GET.get('type') == "student" :
			record = Student.objects.filter(ldap=request.session['id'])
			if record : 
				isEmpty = False
				edit = request.GET.get('edit',False)				
				return render(request,"studentProfile.html",{"isEmpty": isEmpty,"record": record[0], "ldap": request.session['id'],  "edit":edit  })
			else:
				isEmpty = True
				return render(request,"studentProfile.html",{"isEmpty": isEmpty, "ldap": request.session['id']})

		elif request.GET.get('type') == "mess" :
			record = MessAuthority.objects.filter(ID=request.session['id'])
			if record : 
				isEmpty = False
				return render(request,"messAuthorityProfile.html",{"isEmpty": isEmpty,"record": record[0], "ID": request.session['id']})
			else:
				isEmpty = True
				return render(request,"messAuthorityProfile.html",{"isEmpty": isEmpty, "ID": request.session['id']})

		else :
			message = "wrong type (student or mess) "
			return render(request,"error.html",{"message": message})

	elif request.method == 'POST':
		if request.POST.get('type') == "student" :
			record = Student.objects.filter(ldap=request.session['id'])
			if record :
				record.delete()
			s = Student(rollNo = request.POST.get('rollNo'), name = request.POST.get('name'), ldap = request.POST.get('ldap'), roomNo = request.POST.get('roomNo'), phoneNo = request.POST.get('phoneNo'))
			s.save()
			return HttpResponseRedirect("/profile/?type=student")
		
		elif request.POST.get('type') == "mess" :
			record = MessAuthority.objects.filter(ID=request.session['id'])
			if record :
				record.delete()
			h  =  Hostel.objects.get(ID=request.POST.get('hostelID'))
			m = MessAuthority(ID = request.session['id'], name = request.POST.get('name'), hostel= h , phoneNo = request.POST.get('phoneNo'))
			m.save()
			return HttpResponseRedirect("/home/")


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

	# elif request.method == 'POST':
		# get hostel id
		# Display wastage stats in the same html






def viewMenu(request):

	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")

	if request.method == 'GET':
		return render(request,"showMenu.html")


	elif request.method == 'POST':
		hostel_food = dict()
		print request.POST.keys()


		# if 'today' in request.POST.keys():
		# 	print "if"
		# 	today = DAYS[datetime.datetime.today().weekday()]
		# 	daySlot = DaySlot.objects.get(mealType__iexact=request.POST.get('mealType'), day__iexact = today)
		# 	allHostels = Menu.objects.extra(select={'myhostel': 'CAST(hostel_id AS INTEGER)'}).filter(daySlot=daySlot).order_by('myhostel')
			
		# 	for entry in allHostels:
		# 	    if entry.myhostel in hostel_food:
		# 	        hostel_food[entry.myhostel].append(entry.food.name)
		# 	    else:
		# 	        hostel_food[entry.myhostel] = [entry.food.name]

	 #        return render(request,"showDaysMenu.html",{"hostel_food":hostel_food.items()})





        if 'week' in request.POST.keys():
        	print "else"
        	print Menu._meta.get_fields()
        	


        	weeklyMenu = Menu.objects.filter(hostel_id=request.POST.get('hostelID')).extra(select={'mydaySlot': 'CAST(hostel_id AS INTEGER)'}).order_by('mydaySlot')
        	

        	for entry in weeklyMenu:
        		if entry.mydaySlot in hostel_food:
			        hostel_food[entry.mydaySlot].append(entry.food.name)
		     	else:
		     		hostel_food[entry.mydaySlot] = [entry.food.name]
			
			return render(request,"showWeeksMenu.html",{"hostel_food":hostel_food})		





