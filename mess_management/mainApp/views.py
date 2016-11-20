from django.shortcuts import render
from django.http import HttpResponseRedirect
import login.views 
from mainApp.models import *
import datetime
from dateutil.parser import parse as parse_date


# Create your views here.

DAYS = {0:'monday', 1:'tuesday', 2:'wednesday', 3:'thursday', 4:'friday', 5:'saturday', 6:'sunday'}
MEAL_TYPE = ['Breakfast','Lunch','Tiffin','Dinner']

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

		elif request.GET.get('type') == "caterer" :
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
				tempRecord  = record[0]
				record.delete()
			record = Student.objects.filter(rollNo=request.POST.get('rollNo'))	
			
			if record : 
				message = "Roll No already present"
				tempRecord.save()
				return render(request,"error.html",{"message": message})

			s = Student(rollNo = request.POST.get('rollNo'), name = request.POST.get('name'), ldap = request.POST.get('ldap'), roomNo = request.POST.get('roomNo'), phoneNo = request.POST.get('phoneNo'))
			s.save()
			return HttpResponseRedirect("/profile/?type=student")
		
		elif request.POST.get('type') == "caterer" :
			record = MessAuthority.objects.filter(ID=request.session['id'])
			if record :
				record.delete()
			h  =  Hostel.objects.get(ID=request.POST.get('hostelID'))
			m = MessAuthority(ID = request.session['id'], name = request.POST.get('name'), hostel= h , phoneNo = request.POST.get('phoneNo'))
			m.save()
			return HttpResponseRedirect("/profile/?type=caterer")


# Function to display stats

def dispStats(request):

	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")

	studentRecord = Student.objects.filter(ldap=request.session['id'])
	if not studentRecord : 
		return HttpResponseRedirect("/profile/?type=student")

	message = 'Under Maintenance'
	return render(request,"error.html", {'message' : message})


	# if request.method == 'GET':
	# 	record = Student.objects.filter(ldap=request.session['id'])
	# 	if record :
	# 		return render(request,"dispStats.html")

	# 	else:
	# 		isEmpty = True
	# 		return render(request,"profile.html",{"isEmpty": isEmpty,"record": record})

	# elif request.method == 'POST':
	# 	# get hostel id
	# 	# Display wastage stats in the same html
	# 	return render(request,"dispStats.html")		



def showDaysMenu(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")
	studentRecord = Student.objects.filter(ldap=request.session['id'])
	if not studentRecord : 
		return HttpResponseRedirect("/profile/?type=student")
	# if request.method == 'GET':
	    
	#return render(request, "showDaysMenu.html")
	hostel_food = None
	chosen_mealType = None
	if (request.GET.get('action')):
		hostel_food={}
		chosen_mealType = request.GET.get('mealType')
		# print "screwed", 'week' in request.POST
		today = DAYS[datetime.datetime.today().weekday()]
		daySlot = DaySlot.objects.get(mealType__iexact=request.GET.get('mealType'), day__iexact = today)
		allHostels = Menu.objects.extra(select={'myhostel': 'CAST(hostel_id AS INTEGER)'}).filter(daySlot=daySlot).order_by('myhostel')	
		for entry in allHostels:
			if entry.myhostel in hostel_food:
				hostel_food[entry.myhostel].append(entry.food.name)
			else:
				hostel_food[entry.myhostel] = [entry.food.name]
			# print "screwed 2", hostel_food
		hostel_food = sorted(hostel_food.items())
	return render(request,"showDaysMenu.html",{"hostel_food":hostel_food, "chosen_mealType":chosen_mealType})	

def showWeeksMenu(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")
	studentRecord = Student.objects.filter(ldap=request.session['id'])
	if not studentRecord : 
		return HttpResponseRedirect("/profile/?type=student")
	# if request.method == 'GET':
	    
	#return render(request, "showWeeksMenu.html")
	hostel_food = None
	chosen_hostel = None	
	if (request.GET.get('action')):
		hostel_food=[]
		chosen_hostel = request.GET.get('hostelID')
	        # print "in week",request.POST
	        weeklyMenu = Menu.objects.filter(hostel_id=request.GET.get('hostelID'))
	        for j in range(4):
			l = []
			for i in range(7*j,7*(j+1)):
				l1 = []
				for entry in weeklyMenu:
					if (int(entry.daySlot.ID) == (i+1)):#as dayslot id's in Database start from 1
						l1.append(entry.food.name)
						# print "l1    ",l1
				l.append(l1)
			hostel_food.append((MEAL_TYPE[j],l))
	return render(request,"showWeeksMenu.html",{"hostel_food":hostel_food,"chosen_hostel":chosen_hostel})
	# if request.method == 'POST':

# def viewMenu(request):

# 	loggedIn = login.views.validate(request)
# 	if not loggedIn:
# 		return HttpResponseRedirect("/login/")

# 	studentRecord = Student.objects.filter(ldap=request.session['id'])
# 	if not studentRecord : 
# 		return HttpResponseRedirect("/profile/?type=student")

# 	if request.method == 'GET':
# 		return render(request,"showMenu.html")


# 	elif request.method == 'POST':
# 		# print request.POST['action']
# 		# print "yoooooo",'week' in request.POST
# 		if (request.POST['action'] == 'today'):
# 			hostel_food={}
# 			# print "screwed", 'week' in request.POST
# 			today = DAYS[datetime.datetime.today().weekday()]
# 			daySlot = DaySlot.objects.get(mealType__iexact=request.POST.get('mealType'), day__iexact = today)
# 			allHostels = Menu.objects.extra(select={'myhostel': 'CAST(hostel_id AS INTEGER)'}).filter(daySlot=daySlot).order_by('myhostel')	
# 			for entry in allHostels:
# 				if entry.myhostel in hostel_food:
# 					hostel_food[entry.myhostel].append(entry.food.name)
# 				else:
# 					hostel_food[entry.myhostel] = [entry.food.name]

# 			# print "screwed 2", hostel_food
# 			return render(request,"showDaysMenu.html",{"hostel_food":sorted(hostel_food.items())})


# 		if (request.POST['action'] == 'week'):
# 	        	hostel_food=[]
# 	        	# print "in week",request.POST
# 	        	weeklyMenu = Menu.objects.filter(hostel_id=request.POST.get('hostelID'))
# 	        	for j in range(4):
# 				l = []
# 				for i in range(7*j,7*(j+1)):
# 					l1 = []
# 					for entry in weeklyMenu:
# 						if (int(entry.daySlot.ID) == (i+1)):#as dayslot id's in Database start from 1
# 							l1.append(entry.food.name)
# 							# print "l1    ",l1
# 					l.append(l1)
# 				hostel_food.append((MEAL_TYPE[j],l))
# 			return render(request,"showWeeksMenu.html",{"hostel_food":hostel_food})





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


def compare(s,sm,e,em):
	mealTypes = ["breakfast","lunch","tiffin","dinner"] 
	i = mealTypes.index(sm)
	j = mealTypes.index(em)
	if s > e :
		return 1
	if s < e :
		return -1

	return (i > j) - (i < j)

def tempOpt(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")

	studentRecord = Student.objects.filter(ldap=request.session['id'])
	if not studentRecord : 
		return HttpResponseRedirect("/profile/?type=student")

	else : 
		if request.method == 'GET':	
			records = Hostel.objects.all()
			return render(request,"tempOpt.html",{"records" : records})

		elif request.method == 'POST':
			hostelID= request.POST.get('hostelID')
			startDate= parse_date(request.POST.get('startDate')).date()
			startMealType= request.POST.get('startMealType')
			endDate= parse_date(request.POST.get('endDate')).date()
			endMealType= request.POST.get('endMealType')

			tempOpts = TempOpt.objects.filter(student__rollNo = studentRecord[0].rollNo)

			for tempOptRecord in tempOpts :
				tstartDate = tempOptRecord.startDate
				tstartMealType = tempOptRecord.startMealType
				tendDate = tempOptRecord.endDate
				tendMealType =tempOptRecord.endMealType

				if compare(startDate,startMealType,endDate,endMealType) == 1 :
					message = 'Enter correct date/meal type'
					return render(request,"error.html", {'message' : message})

				if ( compare(startDate,startMealType,tendDate,tendMealType) <=0  and compare(endDate,endMealType,tendDate,tendMealType) >=0 ) or ( compare(tstartDate,tstartMealType,endDate,endMealType) <=0 and compare(tendDate,tendMealType,endDate,endMealType) >=0 ) :
					message = 'Overlapping entry already present'
					return render(request,"error.html", {'message' : message})

			hostel = Hostel.objects.get(ID = hostelID)
			if not hostel : 
				message = 'Hostel not Present'
				return render(request,"error.html", {'message' : message})
			t = TempOpt(student = studentRecord[0], hostel = hostel, startDate = startDate, endDate = endDate, startMealType = startMealType, endMealType = endMealType )
			t.save()

			records =  TempOpt.objects.filter(student__rollNo = studentRecord[0].rollNo)

			return render(request,"responseRecorded.html",{"records": records})



#compare only overlapping between holidays
#hostel is null means holiday
def holiday(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")

	studentRecord = Student.objects.filter(ldap=request.session['id'])
	if not studentRecord : 
		return HttpResponseRedirect("/profile/?type=student")

	else : 
		if request.method == 'GET':	
			return render(request,"holiday.html")

		elif request.method == 'POST':
			startDate= parse_date(request.POST.get('startDate')).date()
			startMealType= request.POST.get('startMealType')
			endDate= parse_date(request.POST.get('endDate')).date()
			endMealType= request.POST.get('endMealType')

			tempOpts = TempOpt.objects.filter(student__rollNo = studentRecord[0].rollNo, hostel__isnull = True)

			for tempOptRecord in tempOpts :
				tstartDate = tempOptRecord.startDate
				tstartMealType = tempOptRecord.startMealType
				tendDate = tempOptRecord.endDate
				tendMealType =tempOptRecord.endMealType

				if compare(startDate,startMealType,endDate,endMealType) == 1 :
					message = 'Enter correct date/meal type'
					return render(request,"error.html", {'message' : message})

				if ( compare(startDate,startMealType,tendDate,tendMealType) <=0  and compare(endDate,endMealType,tendDate,tendMealType) >=0 ) or ( compare(tstartDate,tstartMealType,endDate,endMealType) <=0 and compare(tendDate,tendMealType,endDate,endMealType) >=0 ) :
					message = 'Overlapping entry already present'
					return render(request,"error.html", {'message' : message})

			t = TempOpt(student = studentRecord[0], startDate = startDate, endDate = endDate, startMealType = startMealType, endMealType = endMealType )
			t.save()
			records =  TempOpt.objects.filter(student__rollNo = studentRecord[0].rollNo, hostel__isnull = False)
			return render(request,"holidayView.html",{"records": records})






def account(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")
	ldapID = request.session['id']
	studentRecord = Student.objects.filter(ldap = ldapID)
	if not studentRecord : 
		return HttpResponseRedirect("/profile/?type=student")

	else : 
		if request.method == 'GET':
			ldap = request.session['id']
			account = MessAccounts.objects.get(student__rollNo = studentRecord[0].rollNo)
			# print account.balance

			return render(request,"accountDetails.html",{"record": studentRecord[0], "ldap": ldapID , "accNo":account.accountNo,"balance": account.balance })

		# This will never happen
		elif request.method == 'POST':
			return render(request,"accountDetails.html",{"record": studentRecord[0], "ldap": request.session['id']  })



def reg(request):

	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")

	studentRecord = Student.objects.filter(ldap=request.session['id'])
	if not studentRecord : 
		return HttpResponseRedirect("/profile/?type=student")

	
