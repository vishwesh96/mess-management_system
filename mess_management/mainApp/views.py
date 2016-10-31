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
		if 'today' in request.POST:

			today = DAYS[datetime.datetime.today().weekday()]
			daySlot = DaySlot.objects.get(mealType__iexact=request.POST.get('mealType'), day__iexact = today)
			allHostels = Menu.objects.filter(daySlot = daySlot)
			

			for entry in allHostels:
			    if entry.hostel.ID in hostel_food:
			        hostel_food[entry.hostel.ID].append(entry.food.name)
			    else:
			        hostel_food[entry.hostel.ID] = [entry.food.name]
			keys = hostel_food.keys()
			keys.sort()
	        return render(request,"showDaysMenu.html",{"hostel_food":hostel_food, "keys":keys})

        elif 'week' in request.POST:
			weeklyMenu = Menu.objects.filter(hostel_id=request.POST.get('hostelID'))

			for entry in weeklyMenu:
			    if entry.daySlot.ID in hostel_food:
			        hostel_food[entry.daySlot.ID].append(entry.food.name)
			    else:
			        hostel_food[entry.daySlot.ID] = [entry.food.name]
			keys = hostel_food.keys()
			keys.sort()

			return render(request,"showWeeksMenu.html",{"hostel_food":hostel_food, "keys":keys})




# 	if request.method == 'POST':
# 		form = MenuForm(data=request.POST)
# 		result_list = Menu.objects.get(hostel = equest.hostel)
# 		return render(request, 'menu.html',{'form':form,'result_list': result_list})		


# def branchpred(request):
# 	if request.method == 'POST':
# 		form = PredictionForm(data=request.POST)
# 		data=request.POST
# 		rank = data['rank']
# 		institute = data['institute']
# 		category = data['category']
# 		result = []

# 		for j in range(0,len(pata)):
# 			if database_[j][0].find(institute)>=0 or institute.find(database_[j][0])>=0 :
# 				if int(pata[j][2*int(category)]) > int(rank) :
# 					result.append(database[j])
# 		return render(request, 'chutzpah/branchpred.html',{'form':form,'result': result})
# 	else:
# 		form = PredictionForm()
# 	return render(request, 'chutzpah/branchpred.html',{'form': form})	
# def modifyBranch(request):
#     context = RequestContext(request)
#     if request.method == 'POST':
#         form = UserBranchModifyForm(data=request.POST)
#         data=request.POST
#         if form.is_valid():
#             branch = request.POST['currentBranch']
#             currentUser = UserProfile.objects.get(user=request.user)
#             currentUser.currentBranch = branch
#             currentUser.save()
#             return HttpResponseRedirect('/slider/')
#     else:
#         form = UserBranchModifyForm() 
#     return render_to_response(
#             'slider/modifyBranch.html',
#             {'form':form, 'create':True},
#             context)


# 	return render(request,"showMenu.html")
