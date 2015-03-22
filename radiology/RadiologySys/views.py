from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.template import *
from django.shortcuts import *
from RadiologySys.models import *

# Create your views here.
def index(request):
	template = loader.get_template('RadiologySys/index.html')
	context = RequestContext(request)
	return HttpResponse(template.render(context))

# This code was inspired by a tutorial at 'tangowithdjango.com'
def user_login(request):
	context = RequestContext(request)

	if request.method == 'POST':

		#get username and password
		username = request.POST['username']
		password = request.POST['password']

		#user returned if valid
		user = authenticate(username=username, password=password)

		if user:
			# if account is active
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect('/RadiologySys/')
			else:
				return HttpResponse("Error: Account not active")
		else:
			print("Invalid login credentials: {0}, {1}".format(username, password))
			return HttpResponse("Invalid Login, Please Try Again")
	else:
		return render_to_response('RadiologySys/login.html', {}, context)