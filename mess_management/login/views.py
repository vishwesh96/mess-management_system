from django.shortcuts import render
import ldap
# Create your views here.


def login(request):
	if request.method == 'GET':
	    
	    return render(request, "login.html")			##lol

	if request.method == 'POST':
	    
	    userLDAP = request.POST.get("ldapid")
	    userPASS = request.POST.get("ldappass")

	    # if userLDAP == "" or userPASS == "":
	    # 	return render(request,"bcapp/login.html", {"ldapid":userLDAP,"error":"Both fields must be filled!"})

	    (auth,rollno) = doLogin(userLDAP, userPASS)

	    if auth:
    		return render(request,"result.html", {"result": "login successful"})
	    else:
	    	return render(request,"result.html", {"result": "login failed"})


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
