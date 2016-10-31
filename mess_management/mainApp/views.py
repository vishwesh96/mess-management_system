from django.shortcuts import render
from django.http import HttpResponseRedirect
import login.views 
from mainApp.models import *

# Create your views here.


def home(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")

	# if request.method == 'GET':
	    
	return render(request, "home.html")		##lol

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


	return render(request,"showMenu.html")