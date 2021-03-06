from django.shortcuts import render
import ldap
import json
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
# Create your views here.

def welcome(request):
	loggedIn = validate(request)
	if loggedIn:
		return HttpResponseRedirect("/home/")	
	if request.method == 'GET':	    
	    return render(request, "welcome.html")			##lol

	if request.method == 'POST':
		#check if student or caterer and redirect to them appropirately
		if 'studentLogin' in request.POST:
			return HttpResponseRedirect("/loginStudent/")
		elif 'messAuthorityLogin' in request.POST:
			return HttpResponseRedirect("/loginMessAuthority/")




def loginStudent(request):
	loggedIn = validate(request)
	if loggedIn:
		return HttpResponseRedirect("/home/")


	if request.method == 'GET':
	    
	    return render(request, "loginStudent.html")			##lol

	if request.method == 'POST':
	    
	    userLDAP = request.POST.get("ldapid")
	    userPASS = request.POST.get("ldappass")

	    # if userLDAP == "" or userPASS == "":
	    # 	return render(request,"bcapp/login.html", {"ldapid":userLDAP,"error":"Both fields must be filled!"})

	    (auth,rollno) = doLogin(userLDAP, userPASS)				
	    # auth = True	
	    data = {}												#comment to turn on ldap login
	    if auth:
	    	request.session['id'] = userLDAP
	    	request.session['loginType'] = "Student"
	    	data['valid'] = "true"
	    	return HttpResponse(json.dumps(data), content_type = "application/json")
	    else:
	    	data['valid'] = "false"
	    	return HttpResponse(json.dumps(data), content_type = "application/json")

def logout(request):
    try:
        del request.session['id']
    except KeyError:
        pass
    return HttpResponseRedirect("/login/")


def doLogin(userName, passWord):

	userName = "uid="+userName
	conn = ldap.initialize('ldap://ldap.iitb.ac.in')
	search_result = conn.search_s('dc=iitb,dc=ac,dc=in', ldap.SCOPE_SUBTREE, userName, ['uid','employeeNumber'])
	
	try:
		if search_result:
			authenticate = conn.bind_s(search_result[0][0],passWord)
			return(True, search_result[0][1]['employeeNumber'][0])
		else:
			return (False, "")

	except ldap.INVALID_CREDENTIALS:
		return (False, "")

def validate(request): #this is common to both student and caterer as this is checking for only id.
	if (request.session.get('id') is None) or  (request.session.get('loginType') is None):
		return False
	else:
		return True





#caterer login and registration

def loginMessAuthority(request):

	loggedInMessAuthority = validate(request)
	if loggedInMessAuthority:
		return HttpResponseRedirect("/home/")


	if request.method == 'GET':
	    
	    return render(request, "loginMessAuthority.html")			

	if request.method == 'POST':
	    
	    userNAME = request.POST.get("messAuthorityid")
	    userPASS = request.POST.get("messAuthoritypass")

	    auth = authenticate(username=userNAME, password=userPASS)
	    data = {}												#comment to turn on ldap login
	    if auth is not None:
	    	request.session['id'] = userNAME
	    	request.session['loginType'] = "MessAuthority"
	    	data['valid'] = "true"	    	
	    	return HttpResponse(json.dumps(data), content_type = "application/json")
	    else:
	    	data['valid'] = "false"	    		    	
	    	return HttpResponse(json.dumps(data), content_type = "application/json")

def logout(request):
    try:
        del request.session['id']
        del request.session['loginType']
    except KeyError:
        pass
    return HttpResponseRedirect("/welcome/")


# def doLogin(userName, passWord):

# 	userName = "uid="+userName
# 	conn = ldap.initialize('ldap://ldap.iitb.ac.in')
# 	search_result = conn.search_s('dc=iitb,dc=ac,dc=in', ldap.SCOPE_SUBTREE, userName, ['uid','employeeNumber'])
	
# 	try:
# 		if search_result:
# 			authenticate = conn.bind_s(search_result[0][0],passWord)
# 			return(True, search_result[0][1]['employeeNumber'][0])
# 		else:
# 			return (False, "")

# 	except ldap.INVALID_CREDENTIALS:
# 		return (False, "")
