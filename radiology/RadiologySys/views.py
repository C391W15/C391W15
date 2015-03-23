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

	if not request.user.is_authenticated():

		return HttpResponse(template.render(context))

	else:

		if request.method == 'POST':

			pass1 = request.POST['password1']
			pass2 = request.POST['password2']

			if pass1 == pass2:

				request.user.set_password(pass1)
				request.user.save()
				return render_to_response('RadiologySys/home.html', {}, context)

			else:

				return HttpResponse("Passwords Don't Match, Please Try Again")
		else:

			return render_to_response('RadiologySys/home.html', {}, context)

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
				return HttpResponseRedirect('/home/')
			else:
				return HttpResponse("Error: Account not active")
		else:
			print("Invalid login credentials: {0}, {1}".format(username, password))
			return HttpResponse("Invalid Login, Please Try Again")
	else:
		return render_to_response('RadiologySys/login.html', {}, context)




