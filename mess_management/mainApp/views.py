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

	# else if request.method == 'POST':
		# get hostel id
		# Display wastage stats in the same html

def Menu(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")

	if request.method == 'POST':
		form = MenuForm(data=request.POST)
		result_list = Menu.objects.get(hostel = equest.hostel)
		return render(request, 'menu.html',{'form':form,'result_list': result_list})		


def branchpred(request):
	if request.method == 'POST':
		form = PredictionForm(data=request.POST)
		data=request.POST
		rank = data['rank']
		institute = data['institute']
		category = data['category']
		result = []

		for j in range(0,len(pata)):
			if database_[j][0].find(institute)>=0 or institute.find(database_[j][0])>=0 :
				if int(pata[j][2*int(category)]) > int(rank) :
					result.append(database[j])
		return render(request, 'chutzpah/branchpred.html',{'form':form,'result': result})
	else:
		form = PredictionForm()
	return render(request, 'chutzpah/branchpred.html',{'form': form})	
def modifyBranch(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = UserBranchModifyForm(data=request.POST)
        data=request.POST
        if form.is_valid():
            branch = request.POST['currentBranch']
            currentUser = UserProfile.objects.get(user=request.user)
            currentUser.currentBranch = branch
            currentUser.save()
            return HttpResponseRedirect('/slider/')
    else:
        form = UserBranchModifyForm() 
    return render_to_response(
            'slider/modifyBranch.html',
            {'form':form, 'create':True},
            context)