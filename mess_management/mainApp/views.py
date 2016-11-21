from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import login.views 
import json
from mainApp.models import *
import datetime
from dateutil.parser import parse as parse_date
import time
from django.db.models import Q


#global variable decided by Mess authority to allow students to Register towards the begining of every semester
canRegisterHostelAndAccount = True

# Create your views here.

DAYS = {0:'monday', 1:'tuesday', 2:'wednesday', 3:'thursday', 4:'friday', 5:'saturday', 6:'sunday'}
MEAL_TYPE = ['Breakfast','Lunch','Tiffin','Dinner']

def home(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")

	# if request.method == 'GET':
	    
	return render(request, "home.html",{"loginType" : request.session['loginType']})	

	# if request.method == 'POST':


def chooseExtras(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")

	# if request.method == 'GET':
	    
	return render(request, "chooseExtras.html",{"loginType" : request.session['loginType']})

def profile(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")

	loginType = request.GET.get('type')

	# If else is needed when user directly types url corresponding to profile
	
	if request.session['loginType'] == "Student":
		loginType = "student"

	else:
		loginType = "messAuthority"


	if request.method == 'GET':	
		if loginType == "student" :
			record = Student.objects.filter(ldap=request.session['id'])
			if record : 
				isEmpty = False
				edit = request.GET.get('edit',False)

				belongsToRecord = BelongsTo.objects.filter(student = record[0], endDate__isnull = True)
				

				if belongsToRecord:
					hostelNo = belongsToRecord[0].hostel.ID
				else:
					hostelNo = ""

				messAccountRecord = MessAccounts.objects.filter(student = record[0])

				if messAccountRecord:
					messAccountNo = messAccountRecord[0].accountNo
				else:
					messAccountNo = ""
				
				return render(request,"studentProfile.html",{"isEmpty": isEmpty,"record": record[0], "ldap": request.session['id'],  "edit":edit , "loginType" : request.session['loginType'], "canRegisterHostelAndAccount":canRegisterHostelAndAccount, "hostelNo":hostelNo, "messAccountNo":messAccountNo })
			else:
				isEmpty = True
				return render(request,"studentProfile.html",{"isEmpty": isEmpty, "ldap": request.session['id'], "loginType" : request.session['loginType']})

		elif loginType == "messAuthority" :
			record = MessAuthority.objects.filter(ID=request.session['id'])
			if record : 
				isEmpty = False
				edit = request.GET.get('edit',False)
				return render(request,"studentProfile.html",{"isEmpty": isEmpty,"record": record[0], "ID": request.session['id'], "edit":edit,  "loginType" : request.session['loginType']})
			else:
				isEmpty = True
				return render(request,"studentProfile.html",{"isEmpty": isEmpty, "ID": request.session['id'], "loginType" : request.session['loginType'] })

		else :
			message = "wrong type (student or messAuthority) "
			return render(request,"error.html",{"message": message, "loginType" : request.session['loginType']})

	elif request.method == 'POST':  #to do : saving hostelno and messaccountno in db
		if loginType == "student" :

			record = Student.objects.filter(rollNo=request.POST.get('rollNo')).exclude(ldap = request.session['id'])	
			
			if record : 
				message = "Roll No already present"
				return render(request,"error.html",{"message": message, "loginType" : request.session['loginType']})

			
			record = Student.objects.filter(ldap=request.session['id'])

			# print len(s)
			if record:
				s = record[0]
				s.name = request.POST.get('name')
				s.rollNo = request.POST.get('rollNo')
				s.roomNo = request.POST.get('roomNo')
				s.phoneNo = request.POST.get('phoneNo')

			else:
				s = Student(rollNo = request.POST.get('rollNo'), name = request.POST.get('name'), ldap = request.POST.get('ldap'), roomNo = request.POST.get('roomNo'), phoneNo = request.POST.get('phoneNo'))
							
			s.save()

			# retrive hostel record
			h = Hostel.objects.get(ID = request.POST.get('hostelNo'))
			startDate = datetime.datetime.now().date()

			# If student already belongs to a hostel then initialise his end date as today's date and add
			# a new record with the student's new hostel. 

			record = BelongsTo.objects.filter(student = s, endDate__isnull = True)

			
			if record :
				if record[0].hostel.ID != request.POST.get('hostelNo'):
					record[0].endDate = startDate
					record[0].save()
					insertBelongsTo = BelongsTo(student = s, hostel = h, startDate = startDate )
					insertBelongsTo.save()
				

			else:
				insertBelongsTo = BelongsTo(student = s, hostel = h, startDate = startDate )
				# Save record in belongs to
				insertBelongsTo.save()

			# Assumption: When student pays his fees he is given an account number which has the
			# balance equal to fee amount paid. This could be transfered to bank. If he creates 
			# new bank account and links, it is his responsibility to
			# claim the remaining amount in previous account 

			accNo = request.POST.get('messAccountNo')
			

			studentAccount = MessAccounts.objects.filter(student = s).exclude(accountNo = accNo)
			# If the student has other account (previous account) Check for its balance to be 0 before removing it.
			# If balance not zero warn user
			if studentAccount:
				if studentAccount[0].balance == 0:
					studentAccount[0].delete()
				else:
					message = "Previous Account Balance is not zero. Claim it and link with new account"
					return render(request,"error.html",{"message": message, "loginType" : request.session['loginType']})

			record = MessAccounts.objects.filter(accountNo = accNo)

			if record:
				if record[0].student != s:
					message = "Account Given to another student also. Contact ASC"
					return render(request,"error.html",{"message": message, "loginType" : request.session['loginType']})

				else:
					record[0].balance = 15000
					record[0].save()
			else:
				studentAccount = MessAccounts.objects.filter(student = s)
				# print studentAccount[0].balance
				# If the student has other account (previous account) Check for its balance to be 0 before removing it.
				# If balance not zero warn user
				if studentAccount:
					if studentAccount[0].balance == 0:
						studentAccount[0].delete()
					else:
						message = "Previous Account Balance is not zero. Claim it and link with new account"
						return render(request,"error.html",{"message": message, "loginType" : request.session['loginType']})


				# if record is not present, new record is inserted. Balance should come from the asc where he paid fees
				# Here it is hardcoded to 15000		
				record = MessAccounts(student = s, accountNo = accNo, balance = 15000)
				record.save()					

			return HttpResponseRedirect("/profile/?type=student")

		
		elif loginType == "messAuthority" :
			record = MessAuthority.objects.filter(ID=request.session['id'])
			h  =  Hostel.objects.get(ID=request.POST.get('hostelID'))

			if record :
				m = record[0]
				m.name = request.POST.get('name')
				m.hostel = h
				m.phoneNo = request.POST.get('phoneNo')

			else:
				m = MessAuthority(ID = request.session['id'], name = request.POST.get('name'), hostel= h , phoneNo = request.POST.get('phoneNo'))
	
			m.save()
			return HttpResponseRedirect("/profile/?type=messAuthority")


# Function to display stats

def dispStats(request):

	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")

	studentRecord = Student.objects.filter(ldap=request.session['id'])
	if not studentRecord : 
		return HttpResponseRedirect("/profile/?type=student")

	# handcraft dictionary
	wastage = {'Monday': 5, 'Tuesday': 6, 'Wedesday': 0, 'Thursday': 4, 'Friday': 4.5, 'Saturday': 3.4, 'Sunday': 9.6}
	# wastage = {'Monday': 5, 'Tuesday': 6}

	return render(request,"dispStats.html", {"loginType" : request.session['loginType'], "wastage": wastage.items()})


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
	    
	hostel_food = None
	chosen_mealType = None

	if request.method == 'GET':
		hostel_food={}
		chosen_mealType = "breakfast"
		today = DAYS[datetime.datetime.today().weekday()]
	
		daySlot = DaySlot.objects.get(mealType__iexact=chosen_mealType, day__iexact = today)
		allHostels = Menu.objects.extra(select={'myhostel': 'CAST(hostel_id AS INTEGER)'}).filter(daySlot=daySlot).order_by('myhostel')	
		for entry in allHostels:
			if entry.myhostel in hostel_food:
				hostel_food[entry.myhostel].append(entry.food.name)
			else:
				hostel_food[entry.myhostel] = [entry.food.name]
			# print "screwed 2", hostel_food
		hostel_food = sorted(hostel_food.items())

		return render(request,"showDaysMenu.html",{"hostel_food":hostel_food, "chosen_mealType":chosen_mealType,"loginType" : request.session['loginType']})	
	
	elif request.method == 'POST':
		hostel_food={}
		chosen_mealType = request.POST.get('mealType')
		today = DAYS[datetime.datetime.today().weekday()]
	
		daySlot = DaySlot.objects.get(mealType__iexact=chosen_mealType, day__iexact = today)
		allHostels = Menu.objects.extra(select={'myhostel': 'CAST(hostel_id AS INTEGER)'}).filter(daySlot=daySlot).order_by('myhostel')	
		for entry in allHostels:
			if entry.myhostel in hostel_food:
				hostel_food[entry.myhostel].append(entry.food.name)
			else:
				hostel_food[entry.myhostel] = [entry.food.name]

		hostel_food = sorted(hostel_food.items())
		return render(request,"showDaysMenuPost.html",{"hostel_food":hostel_food, "chosen_mealType":chosen_mealType,"loginType" : request.session['loginType']})	

def showWeeksMenu(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")
	studentRecord = Student.objects.filter(ldap=request.session['id'])
	if not studentRecord : 
		return HttpResponseRedirect("/profile/?type=student")

	hostel_food = None
	chosen_hostel = None	
		    
	if request.method == 'GET':
		hostel_food=[]
		chosen_hostel = BelongsTo.objects.filter(student__rollNo=studentRecord[0].rollNo)[0].hostel.ID

	        # print "in week",request.POST
	        weeklyMenu = Menu.objects.filter(hostel_id=chosen_hostel)
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
		return render(request,"showWeeksMenu.html",{"hostel_food":hostel_food,"chosen_hostel":chosen_hostel, "loginType" : request.session['loginType']})

	elif request.method == 'POST':
		hostel_food=[]
		chosen_hostel = request.POST.get('hostelID')
	        # print "in week",request.POST
	        weeklyMenu = Menu.objects.filter(hostel_id=chosen_hostel)
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
		return render(request,"showWeeksMenuPost.html",{"hostel_food":hostel_food,"chosen_hostel":chosen_hostel, "loginType" : request.session['loginType']})


def reviewAndRate(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")

	loginType = request.GET.get('type')

	# If else is needed when user directly types url corresponding to profile
	
	if request.session['loginType'] == "Student":
		loginType = "student"

	else:
		loginType = "messAuthority"


	if request.method == 'GET':	
		if loginType == "student" :
			return render(request,"reviewAndRate.html",{ "loginType" : request.session['loginType'] })

	elif request.method == 'POST':  
		if loginType == "student" :
			record = Student.objects.filter(ldap=request.session['id'])
			if record :
				tempRecord  = record[0]  
				record.delete()
			record = Student.objects.filter(rollNo=request.POST.get('rollNo'))	
			
			if record : 
				message = "Roll No already present"
				tempRecord.save()
				return render(request,"error.html",{"message": message, "loginType" : request.session['loginType']})

			s = Student(rollNo = request.POST.get('rollNo'), name = request.POST.get('name'), ldap = request.POST.get('ldap'), roomNo = request.POST.get('roomNo'), phoneNo = request.POST.get('phoneNo'))
			s.save()
			return HttpResponseRedirect("/profile/?type=student")
		
		elif loginType == "messAuthority" :
			record = MessAuthority.objects.filter(ID=request.session['id'])
			print record
			if record :
				record.delete()

			h  =  Hostel.objects.get(ID=request.POST.get('hostelID'))
			m = MessAuthority(ID = request.session['id'], name = request.POST.get('name'), hostel= h , phoneNo = request.POST.get('phoneNo'))
			m.save()
			return HttpResponseRedirect("/profile/?type=messAuthority")

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
			return render(request,"tempOpt.html",{"records" : records,"loginType" : request.session['loginType']})

		elif request.method == 'POST':
			hostelID= request.POST.get('hostelID')
			startDate= parse_date(request.POST.get('startDate')).date()
			startMealType= request.POST.get('startMealType')
			endDate= parse_date(request.POST.get('endDate')).date()
			endMealType= request.POST.get('endMealType')

			tempOpts = TempOpt.objects.filter(student__rollNo = studentRecord[0].rollNo)

			data = {}
		  
			for tempOptRecord in tempOpts :
				tstartDate = tempOptRecord.startDate
				tstartMealType = tempOptRecord.startMealType
				tendDate = tempOptRecord.endDate
				tendMealType =tempOptRecord.endMealType

				if compare(startDate,startMealType,endDate,endMealType) == 1 :
					data['message'] = 'Enter correct date/meal type'
					return HttpResponse(json.dumps(data), content_type = "application/json")

				if ( compare(startDate,startMealType,tendDate,tendMealType) <=0  and compare(endDate,endMealType,tendDate,tendMealType) >=0 ) or ( compare(tstartDate,tstartMealType,endDate,endMealType) <=0 and compare(tendDate,tendMealType,endDate,endMealType) >=0 ) :
					data['message'] = 'Overlapping entry already present'
					return HttpResponse(json.dumps(data), content_type = "application/json")


			hostel = Hostel.objects.get(ID = hostelID)
			if not hostel : 
				data['message'] = 'Hostel not Present'
		   		return HttpResponse(json.dumps(data), content_type = "application/json")

			t = TempOpt(student = studentRecord[0], hostel = hostel, startDate = startDate, endDate = endDate, startMealType = startMealType, endMealType = endMealType )
			t.save()

			records =  TempOpt.objects.filter(student__rollNo = studentRecord[0].rollNo)

			return render(request,"responseRecordedPost.html",{"records": records, "loginType" : request.session['loginType']})



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
			return render(request,"holiday.html", {"loginType" : request.session['loginType']})

		elif request.method == 'POST':
			startDate= parse_date(request.POST.get('startDate')).date()
			startMealType= request.POST.get('startMealType')
			endDate= parse_date(request.POST.get('endDate')).date()
			endMealType= request.POST.get('endMealType')

			tempOpts = TempOpt.objects.filter(student__rollNo = studentRecord[0].rollNo, hostel__isnull = True)

			data = {}

			for tempOptRecord in tempOpts :
				tstartDate = tempOptRecord.startDate
				tstartMealType = tempOptRecord.startMealType
				tendDate = tempOptRecord.endDate
				tendMealType =tempOptRecord.endMealType

				if compare(startDate,startMealType,endDate,endMealType) == 1 :
					data['message'] = 'Enter correct date/meal type'
					return HttpResponse(json.dumps(data), content_type = "application/json")

				if ( compare(startDate,startMealType,tendDate,tendMealType) <=0  and compare(endDate,endMealType,tendDate,tendMealType) >=0 ) or ( compare(tstartDate,tstartMealType,endDate,endMealType) <=0 and compare(tendDate,tendMealType,endDate,endMealType) >=0 ) :
					data['message'] = 'Overlapping entry already present'
					return HttpResponse(json.dumps(data), content_type = "application/json")

			t = TempOpt(student = studentRecord[0], startDate = startDate, endDate = endDate, startMealType = startMealType, endMealType = endMealType )
			t.save()
			records =  TempOpt.objects.filter(student__rollNo = studentRecord[0].rollNo)
			return render(request,"responseRecordedPost.html",{"records": records, "loginType" : request.session['loginType']})


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

			return render(request,"accountDetails.html",{"record": studentRecord[0], "ldap": ldapID , "accNo":account.accountNo,"balance": account.balance, "loginType" : request.session['loginType'] })

		# This will never happen
		elif request.method == 'POST':
			return render(request,"accountDetails.html",{"record": studentRecord[0], "ldap": request.session['id'] , "loginType" : request.session['loginType'] })



def reg(request):

	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")

	studentRecord = Student.objects.filter(ldap=request.session['id'])
	if not studentRecord : 
		return HttpResponseRedirect("/profile/?type=student")

	

def viewOpt(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")

	studentRecord = Student.objects.filter(ldap=request.session['id'])
	if not studentRecord : 
		return HttpResponseRedirect("/profile/?type=student")


	records =  TempOpt.objects.filter(student__rollNo = studentRecord[0].rollNo)

	return render(request,"responseRecorded.html",{"records": records, "loginType" : request.session['loginType']})


def deleteOpt(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")

	studentRecord = Student.objects.filter(ldap=request.session['id'])
	if not studentRecord : 
		return HttpResponseRedirect("/profile/?type=student")


	hostelID = request.GET.get('hostelID')
	startDate = request.GET.get('startDate')
	startMealType = request.GET.get('startMealType')
	endDate = request.GET.get('endDate')
	endMealType = request.GET.get('endMealType')

	if hostelID == "No hostel opted" : 
		null = True
	else :
		null = False

	print datetime.datetime.now()
	print startDate
	print startMealType
	records =  TempOpt.objects.filter(student__rollNo = studentRecord[0].rollNo)

	return render(request,"responseRecorded.html",{"records": records, "loginType" : request.session['loginType']})

def messAuthorityMenu(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/login/")

	# if request.method == 'GET':
	    	
	return render(request, "messAuthorityMenu.html",{"loginType" : request.session['loginType']})	