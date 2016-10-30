from django.shortcuts import render

# Create your views here.


def home(request):
	if request.method == 'GET':
	    
	    return render(request, "home.html")			##lol

	if request.method == 'POST':

		return render(request,"profile.html")
