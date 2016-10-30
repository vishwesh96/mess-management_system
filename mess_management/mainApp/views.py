from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.


def home(request):
	loggedIn = validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")


	if request.method == 'GET':
	    
	    return render(request, "home.html")		##lol

	if request.method == 'POST':
		# if request.action == 'logout'
			# return HttpResponseRedirect("/login/")
		# else:		
		return render(request,"profile.html")



def validate(request):
	if request.session.get('id') is None:
		return False
	else:
		return True

