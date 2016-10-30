from django.shortcuts import render
import ldap
from django.http import HttpResponseRedirect

# Create your views here.


def login(request):

	loggedIn = validate(request)
	if loggedIn:
		return HttpResponseRedirect("/home/")


	if request.method == 'GET':
	    
	    return render(request, "login.html")			##lol

	if request.method == 'POST':
	    
	    userLDAP = request.POST.get("ldapid")
	    userPASS = request.POST.get("ldappass")

	    # if userLDAP == "" or userPASS == "":
	    # 	return render(request,"bcapp/login.html", {"ldapid":userLDAP,"error":"Both fields must be filled!"})

	    # (auth,rollno) = doLogin(userLDAP, userPASS)				#comment to turn off ldap login
	    auth = True													#comment to turn on ldap login
	    if auth:
	    	request.session['id'] = userLDAP
    		return HttpResponseRedirect("/home/")
	    else:
	    	return render(request,"result.html", {"result": "login failed"})

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

def validate(request):
	if request.session.get('id') is None:
		return False
	else:
		return True
