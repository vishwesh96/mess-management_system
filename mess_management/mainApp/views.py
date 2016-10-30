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
		record = Student.objects.filter(ldap=request.session['id'])
		if record : 
			isEmpty = False
		else:
			isEmpty = True
		return render(request,"profile.html",{"isEmpty": isEmpty,"record": record[0]})
