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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


#global variable decided by Mess authority to allow students to Register towards the begining of every semester
canRegisterHostelAndAccount = True

# Create your views here.

DAYS = {0:'monday', 1:'tuesday', 2:'wednesday', 3:'thursday', 4:'friday', 5:'saturday', 6:'sunday'}
MEAL_TYPE_MAPPING = {'': 0, 'breakfast' : 1, 'lunch': 2, 'tiffin': 3, 'dinner': 4}
MEAL_TYPE = ['Breakfast','Lunch','Tiffin','Dinner']

TIMINGS = [datetime.time(6), datetime.time(10), datetime.time(15,30), datetime.time(18), datetime.time(22)]

# def validate(request,hostel):
# 	loggedIn = login.views.validate(request)
# 	if not loggedIn:
# 		return HttpResponseRedirect("/welcome/")

# 	if request.session['loginType'] == "Student":
# 		studentRecord = Student.objects.filter(ldap=request.session['id'])
# 		if studentRecord : 
# 			hostel = 
# 		else:
# 			return HttpResponseRedirect("/profile/?type=student")
# 	else:
# 		authorityRecord = MessAuthority.objects.filter(id = request.session['id'])
# 		if authorityRecord:





def home(request):

####################################################################
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/welcome/")

	if request.session['loginType'] == "Student":
		studentRecord = Student.objects.filter(ldap=request.session['id'])
		if not studentRecord:
			return HttpResponseRedirect("/profile/?type=student")
		
		else:
			record = BelongsTo.objects.filter(student = studentRecord[0], endDate__isnull = True)
			if record:
				hostel = record[0].hostel
				# record = TempOpt.objects.all()		
				# date = record[0].startDate
			else:
				return render(request, "home.html",{"loginType" : request.session['loginType'], "notifications" : []})		

	
	elif request.session['loginType'] == "MessAuthority":
		authorityRecord = MessAuthority.objects.filter(ID = request.session['id'])
		if not authorityRecord:
			return HttpResponseRedirect("/profile/?type=messAuthority")
		else:
			hostel = authorityRecord[0].hostel

#########################################################################
	
	notifs = []
	notifications=[]
	if request.method == 'GET':
		announcements = Announcement.objects.filter(hostel = hostel).order_by('-dateTime')
		for entry in announcements:
			notifs.append([entry.dateTime, entry.subject, entry.text])


		#code for pagenation
		paginator = Paginator(notifs, 10) # Show 10 contacts per page
		page = request.GET.get('page')
		try:
        		notifications = paginator.page(page)
    		except PageNotAnInteger:
        		# If page is not an integer, deliver first page.
        		notifications = paginator.page(1)
    		except EmptyPage:
        		# If page is out of range (e.g. 9999), deliver last page of results.
        		notifications = paginator.page(paginator.num_pages)

		return render(request, "home.html",{"loginType" : request.session['loginType'], "notifications" : notifications})	


	elif request.method == 'POST':
		record = Announcement.objects.filter(hostel = hostel).order_by('-ID')
		if record:
			id = record[0].ID+1
		else:
			id = 1

		dateTime = datetime.datetime.now()
		a = Announcement(subject = request.POST.get('subject'), text= request.POST.get('text'), hostel = hostel, ID = id, dateTime = dateTime)
		a.save()


		data = {}
		data['time'] = '%s' % dateTime.ctime()
		
		# announcements = Announcement.objects.filter(hostel = hostel).order_by('-dateTime')
		# for entry in announcements:
		# 	notifs.append([entry.dateTime, entry.subject, entry.text])


		# #code for pagenation
		# paginator = Paginator(notifs, 10) # Show 10 contacts per page
		# page = request.GET.get('page')
		# try:
  #       		notifications = paginator.page(page)
  #   		except PageNotAnInteger:
  #       		# If page is not an integer, deliver first page.
  #       		notifications = paginator.page(1)
  #   		except EmptyPage:
  #       		# If page is out of range (e.g. 9999), deliver last page of results.
  #       		notifications = paginator.page(paginator.num_pages)
		return HttpResponse(json.dumps(data), content_type = "application/json")



def editCost(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/welcome/")


	authorityRecord = MessAuthority.objects.filter(ID=request.session['id'])
	if not authorityRecord : 
		return HttpResponseRedirect("/profile/?type=messAuthority")
	else:
		hostel = authorityRecord[0].hostel

	mealCosts = {}

	# If all entries in dictionary needed then use thsi dictionary
	# mealCosts = {'breakfast': 0, 'lunch' : 0, 'tiffin' : 0, 'dinner': 0 }

	if request.method == 'GET':
		record = Cost.objects.filter(hostel = hostel)
		if record:
			for entry in record:
				mealCosts[entry.mealType] = entry.cost

		retData = {}
		retData['costs'] = mealCosts
		# print json.dumps(retData)
		return HttpResponse(json.dumps(retData), content_type = "application/json")


	elif request.method == 'POST':
		for entry in MEAL_TYPE:
			record = Cost.objects.filter(hostel = hostel, mealType = entry.lower())
			if record:
				c = record[0]
				c.cost = request.POST.get(c.mealType)
			else:
				c = Cost(hostel = hostel, mealType = entry.lower(), cost = request.POST.get(entry.lower()))

			c.save()

		data = {}
		data['valid'] = True
		return HttpResponse(json.dumps(data), content_type = "application/json")




def addFood(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/welcome/")


	authorityRecord = MessAuthority.objects.filter(ID=request.session['id'])
	if not authorityRecord : 
		return HttpResponseRedirect("/profile/?type=messAuthority")
	else:
		hostel = authorityRecord[0].hostel

	if request.method == 'GET':
		return HttpResponseRedirect("/home/")

	elif request.method == 'POST':
		record = FoodItem.objects.extra(select={'foodID': 'CAST("ID" AS INTEGER)'}).all().order_by('-foodID')
		if record:
			id = str(record[0].foodID+1)	
		else:
			id = str(1)

		f = FoodItem(ID = id ,name = request.POST.get('name'), type = request.POST.get('type'),quantity = request.POST.get('quantity'),calories = request.POST.get('calories'))
		f.save()

		data = {}
		data['valid'] = True
		return HttpResponse(json.dumps(data), content_type = "application/json")

# Date and mealType intersection with tempOpt 
def checkIntersection(currDate, entry,mealType):
	if currDate > entry.startDate and currDate < entry.endDate:
		return True

	elif currDate == entry.startDate and MEAL_TYPE_MAPPING[mealType] >= MEAL_TYPE_MAPPING[entry.startMealType]:
		if currDate == entry.endDate and MEAL_TYPE_MAPPING[mealType] <= MEAL_TYPE_MAPPING[entry.endMealType]:
			return True

	elif currDate == entry.endDate and MEAL_TYPE_MAPPING[mealType] <= MEAL_TYPE_MAPPING[entry.endMealType]:
		if currDate == entry.startDate and MEAL_TYPE_MAPPING[mealType] >= MEAL_TYPE_MAPPING[entry.startMealType]:
			return True



def dispCount(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/welcome/")


	authorityRecord = MessAuthority.objects.filter(ID=request.session['id'])
	if not authorityRecord : 
		return HttpResponseRedirect("/profile/?type=messAuthority")
	else:
		hostel = authorityRecord[0].hostel

	if request.method == 'GET':


		currTime = datetime.datetime.now().time()
		currDate = datetime.datetime.now().date()

		if currTime > TIMINGS[0] and currTime < TIMINGS[1]:
			mealType = 'breakfast'
		
		elif currTime > TIMINGS[1] and currTime < TIMINGS[2]:
			mealType = 'lunch'
		
		elif currTime > TIMINGS[2] and currTime < TIMINGS[3]:
			mealType = 'tiffin'
		
		elif currTime > TIMINGS[3] and currTime < TIMINGS[4]:
			mealType = 'dinner'

		else:
			mealType = ""


		count = 0
		
		if mealType:
			# Other hostel opted here
			record = TempOpt.objects.filter(hostel = hostel)
			if record :
				for entry in record:
					if checkIntersection(currDate,entry,mealType):
						count = count+1

			# Same hostel not opted out
			record = BelongsTo.objects.filter(hostel = hostel, endDate__isnull = True)
			for entry in record:
				temp = TempOpt.objects.filter(student = entry.student)
				intersection = False
				for t in temp:
					if checkIntersection(currDate, t,mealType):
						intersection = True
						break

				if not intersection:
					count = count + 1

		data = {}
		data['count'] = count
		data['mealType'] = mealType
		return HttpResponse(json.dumps(data), content_type = "application/json")
		# return render(request, "addFood.html",{ "loginType" : request.session['loginType']})



# Function to check the student can be allowed to eat in this hostel

def checkStudent(rollNo, message, hostel):
	record = Student.objects.filter(rollNo = rollNo)
	
	if not record:
		message = "Wrong Roll Number"
		return False

	student = record[0]
	record = BelongsTo.objects.filter(student = student, endDate__isnull = True)
	if not record:
		message.append("Student Not Registered in any hostel")
		return False

	# If student in this hostel and opted out to some other hostel, then deny service
	studentHostel = record[0].hostel
	currDate = 	datetime.datetime.now().date()
	currTime =  datetime.datetime.now().time()

	if currTime > TIMINGS[0] and currTime < TIMINGS[1]:
		mealType = 'breakfast'
	
	elif currTime > TIMINGS[1] and currTime < TIMINGS[2]:
		mealType = 'lunch'
	
	elif currTime > TIMINGS[2] and currTime < TIMINGS[3]:
		mealType = 'tiffin'
	
	elif currTime > TIMINGS[3] and currTime < TIMINGS[4]:
		mealType = 'dinner'

	else:
		mealType = ""



	if studentHostel == hostel:
		record = TempOpt.objects.filter(student = student)
		if not record:
			return True


		for entry in record:
			if checkIntersection(currDate, entry, mealType) :
				message.append("Belongs to this hostel but opted out")
				return False

	else:
		record = TempOpt.objects.filter(student = student, hostel = hostel)
		if not record:
			message.append("Student does not belong and has not opted this hostel today")
			return False

		for entry in record:
			if checkIntersection(currDate, entry, mealType) :
				return True

		message.append("Student has not opted to this hostel")
		return False


def chooseExtras(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/welcome/")


	authorityRecord = MessAuthority.objects.filter(ID=request.session['id'])
	if not authorityRecord : 
		return HttpResponseRedirect("/profile/?type=messAuthority")
	else:
		hostel = authorityRecord[0].hostel


	if request.method == 'GET':

		return render(request, "chooseExtras.html",{"loginType" : request.session['loginType']})

	elif request.method == 'POST':
		data = {}
		if request.POST.get('submit') == 'false':
			name = request.POST.get('data')
			records = FoodItem.objects.filter(name = name)
			if records:
				food = records[0]
			# No else necessary since a case wont occur. If statement just for safety
			e = Extras.objects.filter(hostel = hostel, food = food)

			if e:
				cost = e[0].cost
			# No else necessary since a case wont occur. If statement just for safety
			data['cost'] = cost

		elif request.POST.get('submit') == 'true':

			cost = request.POST.get('data')
			rollNo = request.POST.get('rollNo')

			temp = []
			if checkStudent(rollNo = rollNo, message= temp, hostel = hostel):
				record = Student.objects.filter(rollNo = rollNo)				
				student = record[0]
				account = MessAccounts.objects.filter(student = student)
				if account:
					account[0].balance = account[0].balance - int(cost)
					account[0].save()
					data['valid'] = "true"
				else:
					data['valid'] = "false"
					message = "No account Corresponding to student"					
					data['message'] = message
					# render 

			else:
				data['valid'] = "false"
				data['message'] = "No account Corresponding to student"


		return HttpResponse(json.dumps(data), content_type = "application/json")



# def deductMoney(request):
# 	loggedIn = login.views.validate(request)
# 	if not loggedIn:
# 		return HttpResponseRedirect("/welcome/")


# 	authorityRecord = MessAuthority.objects.filter(ID=request.session['id'])
# 	if not authorityRecord : 
# 		return HttpResponseRedirect("/profile/?type=messAuthority")
# 	else:
# 		hostel = authorityRecord[0].hostel

# 	temp = []
# 	currDate = 	datetime.datetime.now().date()
# 	currTime =  datetime.datetime.now().time()
# 	if currTime > TIMINGS[0] and currTime < TIMINGS[1]:
# 		mealType = 'breakfast'
	
# 	elif currTime > TIMINGS[1] and currTime < TIMINGS[2]:
# 		mealType = 'lunch'
	
# 	elif currTime > TIMINGS[2] and currTime < TIMINGS[3]:
# 		mealType = 'tiffin'
	
# 	elif currTime > TIMINGS[3] and currTime < TIMINGS[4]:
# 		mealType = 'dinner'

# 	else:
# 		mealType = ""



# 	record = Deduct.objects.filter(hostel = hostel)
# 	if not record:
# 		final = Deduct(hostel = hostel, deduct = False, completed = 0)
# 		final.save()
# 	else:
# 		final = record[0]

# 	if (final.completed != MEAL_TYPE_MAPPING[mealType]) and (MEAL_TYPE_MAPPING[mealType] != 0):
# 		final.completed = MEAL_TYPE_MAPPING[mealType]
# 		final.deduct = True
# 		final.save()

# 	if final.deduct:
# 		record = Cost.objects.filter(mealType = mealType, hostel = hostel)
# 		if record:
# 			cost = record[0].cost
# 		else:
# 			cost = 0

# 		# Students of same hostel
# 		record = BelongsTo.objects.filter(hostel = hostel, endDate__isnull = True)
# 		for entry in record:
# 			if checkStudent(rollNo = entry.student.rollNo, hostel = hostel, message = temp):
# 				record = MessAccounts.object.filter(student = entry.student)
# 				if record:
# 					record[0].balance = record[0].balance - cost
# 					record[0].save()


# 		record = TempOpt.objects.filter(hostel = hostel)
# 		for entry in record:
# 			if checkIntersection(entry = entry, mealType = mealType, currDate = currDate):
# 				record = MessAccounts.object.filter(student = entry.student)
# 				if record:
# 					record[0].balance = record[0].balance - cost
# 					record[0].save()

# 		final.deduct = False
# 		final.save()

# 	return HttpResponseRedirect("/welcome/")




def profile(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/welcome/")

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
				
				return render(request,"profile.html",{"isEmpty": isEmpty,"record": record[0], "ldap": request.session['id'],  "edit":edit , "loginType" : request.session['loginType'], "canRegisterHostelAndAccount":canRegisterHostelAndAccount, "hostelNo":hostelNo, "messAccountNo":messAccountNo })
			else:
				isEmpty = True
				return render(request,"profile.html",{"isEmpty": isEmpty, "ldap": request.session['id'], "loginType" : request.session['loginType']})

		elif loginType == "messAuthority" :
			record = MessAuthority.objects.filter(ID=request.session['id'])
			if record : 
				isEmpty = False
				edit = request.GET.get('edit',False)
				return render(request,"profile.html",{"isEmpty": isEmpty,"record": record[0], "ID": request.session['id'], "edit":edit,  "loginType" : request.session['loginType']})
			else:
				isEmpty = True
				return render(request,"profile.html",{"isEmpty": isEmpty, "ID": request.session['id'], "loginType" : request.session['loginType'] })

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
		return HttpResponseRedirect("/welcome/")
	if request.session['loginType'] == "Student":
		studentRecord = Student.objects.filter(ldap=request.session['id'])
		if not studentRecord : 
			return HttpResponseRedirect("/profile/?type=student")
	else:
		authorityRecord = MessAuthority.objects.filter(ID=request.session['id'])
		if not authorityRecord : 
			return HttpResponseRedirect("/profile/?type=messAuthority")


	if request.method == 'GET':
	
		if request.session['loginType'] == "Student":
			belongsTo = BelongsTo.objects.filter(student = studentRecord[0], endDate__isnull =True)
			if belongsTo:
				hostel = belongsTo[0].hostel
			else:
				message = "You Belong to no hostel"
				return render(request,"error.html",{"message": message, "loginType" : request.session['loginType']})
		else:
			hostel = authorityRecord[0].hostel

		w = Wastage.objects.filter(hostel = hostel).order_by('day')
		wastage=[]
		for entry in w:
			if entry.day <= datetime.datetime.today().weekday():
				wastage.append((DAYS[entry.day] ,entry.wasted))

		return render(request,"dispStats.html", {"loginType" : request.session['loginType'], "wastage": wastage})


	# todo after ajax post
	elif request.method == 'POST':
		# get hostel id
		# Display wastage stats in the same html
		currWastage =  request.POST.get('wastage');
		a = Wastage.objects.filter( hostel = authorityRecord[0].hostel, day = datetime.datetime.today().weekday())
		if a:
			w = a[0]
			w.wasted = currWastage	
		else:
			w = Wastage(wasted = currWastage, hostel = authorityRecord[0].hostel, day = datetime.datetime.today().weekday())
		w.save()

		w = Wastage.objects.filter(hostel = authorityRecord[0].hostel).order_by('day')
		wastage=[]
		for entry in w:
			if entry.day <= datetime.datetime.today().weekday():
				wastage.append((DAYS[entry.day] ,entry.wasted))

		return render(request,"dispStatsPost.html", {"currWastage": currWastage ,"loginType" : request.session['loginType'], "wastage": wastage})



def showDaysMenu(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/welcome/")
	studentRecord = Student.objects.filter(ldap=request.session['id'])
	if not studentRecord : 
		return HttpResponseRedirect("/profile/?type=student")
	else:
		record = BelongsTo.objects.filter(student = studentRecord[0], endDate__isnull = True)
		if record:
			hostel = record[0].hostel
		else:
			return HttpResponseRedirect("/profile/?type=student")
	    
	hostel_food = {}
	chosen_mealType = None

	if request.method == 'GET':
		chosen_mealType = "breakfast"
		
	
	elif request.method == 'POST':
		chosen_mealType = request.POST.get('mealType')


	today = DAYS[datetime.datetime.today().weekday()]

	daySlot = DaySlot.objects.get(mealType__iexact=chosen_mealType, day__iexact = today)
	allHostels = Menu.objects.extra(select={'myhostel': 'CAST(hostel_id AS INTEGER)'}).filter(daySlot=daySlot).order_by('myhostel')	

	for entry in allHostels:
		if entry.myhostel in hostel_food:
			hostel_food[entry.myhostel][0].append(entry.food.name)
		else:
			hostel_food[entry.myhostel] = [[entry.food.name]]

		record = Cost.objects.filter(hostel = entry.hostel, mealType = chosen_mealType)
		if record:
			cost = record[0].cost
		else:
			cost = "--"

		sum = 0
		count = 0

		record = Rated.objects.filter(hostel = entry.hostel)
		for e in record:
			sum+=e.overall
			count+=1
		if count == 0:
			rating = 0
		else:
			rating = ((sum)*20)/count

		hostel_food[entry.myhostel].append(cost)
		hostel_food[entry.myhostel].append(rating)

	hostel_food = sorted(hostel_food.items())
	if request.method == 'GET':
		return render(request,"showDaysMenu.html",{"hostel_food":hostel_food, "chosen_mealType":chosen_mealType,"loginType" : request.session['loginType']})		
	
	elif request.method == 'POST':
		return render(request,"showDaysMenuPost.html",{"hostel_food":hostel_food, "chosen_mealType":chosen_mealType,"loginType" : request.session['loginType']})
		


def showWeeksMenu(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/welcome/")
	studentRecord = Student.objects.filter(ldap=request.session['id'])
	if not studentRecord : 
		return HttpResponseRedirect("/profile/?type=student")

	hostel_food = None
	chosen_hostel = None	
		    
	if request.method == 'GET':
		hostel_food=[]
		chosen_hostel = BelongsTo.objects.filter(student__rollNo=studentRecord[0].rollNo, endDate__isnull = True)[0].hostel.ID

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
		return HttpResponseRedirect("/welcome/")

	studentRecord = Student.objects.filter(ldap=request.session['id'])
	if not studentRecord : 
		return HttpResponseRedirect("/profile/?type=student")

	if request.method == 'GET':	
		return render(request,"reviewAndRate.html",{ "loginType" : request.session['loginType'] })

	elif request.method == 'POST': 
		rateType = request.POST.get('type')
		data = request.POST.get('data')
		
		hostel= BelongsTo.objects.filter(student__rollNo=studentRecord[0].rollNo, endDate__isnull = True)[0].hostel
		rating  = Rated.objects.filter(student__rollNo=studentRecord[0].rollNo,hostel__ID=hostel.ID)
		if rating : 		
			record = rating[0]
		else  :
			record = Rated(student=studentRecord[0],hostel=hostel)
		if rateType == "taste" : 
			record.taste =  data
			record.save()
		elif rateType == "costEffective" :
			record.costEffective = data
			record.save()
		elif rateType == "cleanliness" :
			record.cleanliness = data
			record.save()
		elif rateType == "overall" :
			record.overall = data
			record.save()
		elif rateType == "review" :
			reviewRecord = Reviewed(student=studentRecord[0],hostel=hostel)
			reviewRecord.review = data
			reviewRecord.dateTime = datetime.datetime.now()
			if data :
				reviewRecord.save()

		message = "Review Recorded"
		return render(request,"errorPost.html",{"message": message})


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
		return HttpResponseRedirect("/welcome/")

	studentRecord = Student.objects.filter(ldap=request.session['id'])
	if not studentRecord : 
		return HttpResponseRedirect("/profile/?type=student")

	else:
		record = BelongsTo.objects.filter(student = studentRecord[0], endDate__isnull = True)
		if not record:
			return HttpResponseRedirect("/profile/?type=student")
		else:
			hostel = record[0].hostel									

		if request.method == 'GET':	
			records = Hostel.objects.filter(~Q(ID = hostel.ID))
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
		return HttpResponseRedirect("/welcome/")

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
		return HttpResponseRedirect("/welcome/")
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
		return HttpResponseRedirect("/welcome/")

	studentRecord = Student.objects.filter(ldap=request.session['id'])
	if not studentRecord : 
		return HttpResponseRedirect("/profile/?type=student")

	

def viewOpt(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/welcome/")

	studentRecord = Student.objects.filter(ldap=request.session['id'])
	if not studentRecord : 
		return HttpResponseRedirect("/profile/?type=student")


	records =  TempOpt.objects.filter(student__rollNo = studentRecord[0].rollNo)

	return render(request,"responseRecorded.html",{"records": records, "loginType" : request.session['loginType']})


def deleteOpt(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/welcome/")

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

	records =  TempOpt.objects.filter(student__rollNo = studentRecord[0].rollNo)

	return render(request,"responseRecorded.html",{"records": records, "loginType" : request.session['loginType']})



def messAuthorityMenu(request):
	loggedIn = login.views.validate(request)
	if not loggedIn:
		return HttpResponseRedirect("/welcome/")

	authorityRecord = MessAuthority.objects.filter(ID=request.session['id'])
	if authorityRecord:
		chosen_hostel =  authorityRecord[0].hostel
	else:
		return HttpResponseRedirect("/profile/?type=messAuthority")

	hostel_food = []
		    
	if request.method == 'GET':
	        # print "in week",request.POST
	        weeklyMenu = Menu.objects.filter(hostel=chosen_hostel)
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
		all_items = FoodItem.objects.all()
		return render(request,"messAuthorityMenu.html",{"all_items": all_items, "hostel_food":hostel_food,"chosen_hostel":chosen_hostel.ID, "loginType" : request.session['loginType']})

	if request.method == 'POST':
		items =  json.loads(request.POST.get('items'))

		dayslot = DaySlot.objects.get(day = request.POST.get('day').strip(), mealType = request.POST.get('mealType').strip().lower())
		foodItems = Menu.objects.filter(daySlot = dayslot, hostel = chosen_hostel)
		
		for foodItem in foodItems:
			foodItem.delete()

		for item in items:
			food = FoodItem.objects.get(name = item)
			m = Menu(daySlot = dayslot, hostel = chosen_hostel, food = food)
			m.save()


	        # print "in week",request.POST
	        weeklyMenu = Menu.objects.filter(hostel=chosen_hostel)
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
		all_items = FoodItem.objects.all()
		return render(request,"messAuthorityMenuPost.html",{"hostel_food":hostel_food,"loginType" : request.session['loginType']})





