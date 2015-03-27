from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.template import *
from django.shortcuts import *
from RadiologySys.models import *
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.
def index(request):
	context = RequestContext(request)
	return render_to_response('RadiologySys/home.html', {}, context)

def change_info(request):
	context = RequestContext(request)
	
	username = request.session.get('username')
	person = (Users.objects.get(user_name=username)).person_id
	#person = Persons.objects.get(person_id = userPerson_id)
	firstName = person.first_name
	lastName = person.last_name
	address = person.address
	email = person.email
	phone = person.phone

	request.session['first_name'] = firstName
	request.session['last_name'] = lastName
	request.session['address'] = address
	request.session['email'] = email
	request.session['phone'] = phone

	if request.method == 'POST':

		return render_to_response('RadiologySys/changeInfo.html', {}, context)

	else:
		return render_to_response('RadiologySys/changeInfo.html', {}, context)
	



def change_pass(request):
	context = RequestContext(request)
	username = request.session.get('username')
	password = request.session.get('password')

	if request.method == 'POST':

		pass1 = request.POST['password1']
		pass2 = request.POST['password2']

		if pass1 == pass2 and pass1 != "" and pass1 != password:

			user = Users.objects.get(user_name = username)
			user.password = pass1
			user.save()
			messages.success(request, 'Password updated')
			
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
		user = myLogin(username, password)

		if user:
			return HttpResponseRedirect('/home/')

		else:
			print("Invalid login credentials: {0}, {1}".format(username, password))
			messages.warning(request, "Invalid Login, Please Try Again")
			return render_to_response('RadiologySys/login.html', {}, context)
	else:
		return render_to_response('RadiologySys/login.html', {}, context)

def report(request):

	context = RequestContext(request)

	# Requires user to be logged in
	if not request.user.is_authenticated():
		return redirect('/login')

	if request.method == 'POST':

		# Get diagnosis and time frame
		diagnosis = request.POST['diagnosis']
		tstart = request.POST['time_start']
		tend = request.POST['time_end']

		mydictionary = {"diagnosis": diagnosis,
						"tstart": tstart,
						"tend": tend}

		# Ensures valid time frame
		if tstart > tend:
			return HttpResponse("Error: start date after end date")
		else:
			print("rendering" + " " + diagnosis + " " + tstart + " " + tend)
			return render_to_response('RadiologySys/results.html', mydictionary, context)

	else:
		return render_to_response('RadiologySys/report.html', {}, context)


def myLogin(username, password):

	user = Users.objects.get(user_name=username)

	if user.password == password:
		return user
	else: 
		return None




