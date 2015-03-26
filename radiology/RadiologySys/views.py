from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.template import *
from django.shortcuts import *
from RadiologySys.models import *
from django.contrib import messages

# Create your views here.
def index(request):
	context = RequestContext(request)
	return render_to_response('RadiologySys/home.html', {}, context)


def change_pass(request):
	context = RequestContext(request)
	username = request.session.get('username')
	password = request.session.get('password')

	if request.method == 'POST':

		pass1 = request.POST['password1']
		pass2 = request.POST['password2']

		if pass1 == pass2 and pass1 != "" and pass1 != password:

			request.user.set_password(pass1)
			request.user.save()
			messages.success(request, 'Password updated')
			#user = authenticate(username=username, password=pass1)
			#if user:
			#	login(request,user)
			return render_to_response('RadiologySys/changePass.html', {}, context)

		elif pass1 == password:
			messages.warning(request, "Password is the same, Please Try Again")
			return render_to_response('RadiologySys/changePass.html', {}, context)

		else:
			messages.warning(request, "Passwords Don't Match, Please Try Again")
			return render_to_response('RadiologySys/changePass.html', {}, context)

	else:
		return render_to_response('RadiologySys/changePass.html', {}, context)

# This code was inspired by a tutorial at 'tangowithdjango.com'
def user_login(request):
	
	context = RequestContext(request)

	if request.method == 'POST':

		#get username and password
		username = request.POST['username']
		password = request.POST['password']
		request.session['username'] = username
		request.session['password'] = password

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
			messages.warning(request, "Invalid Login, Please Try Again")
			return render_to_response('RadiologySys/login.html', {}, context)
	else:
		return render_to_response('RadiologySys/login.html', {}, context)




