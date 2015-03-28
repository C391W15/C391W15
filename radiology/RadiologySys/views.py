from django.shortcuts import *
from RadiologySys.models import *
from django.shortcuts import redirect
from django.contrib import messages
from RadiologySys.forms import *
from datetime import date
from django.db import connection

# Create your views here.
def index(request):
	context = RequestContext(request)

	myClass = request.session.get('class')

	return render_to_response('RadiologySys/home.html', {'class': myClass}, context)

def user_managment(request):
	context = RequestContext(request)
	request.session['updateUser'] = None
	return render_to_response('RadiologySys/userManagment.html', {}, context)

def update_family_doctor(request):
	context = RequestContext(request)

	if request.method == 'POST':
		form = FamilyDoctorForm(request.POST)
		
		if form.is_valid():			

			doctor = form.cleaned_data['doctor_id']
			patient = form.cleaned_data['patient_id']

			doctor = Users.objects.get(person_id=doctor)
			patient = Users.objects.get(person_id=patient)


			if doctor.classType != 'd' or patient.classType != 'p':
				messages.warning(request, 'Ensure Persons Chosen are Patient/Doctor')
				return render_to_response('RadiologySys/updateFamilyDoctorz.html', {}, context)

			form.save()
			messages.success(request, 'New Doctor/Patient Relationship Added')
			return render_to_response('RadiologySys/updateFamilyDoctor.html', {'form': form}, context) 

		else:
			messages.warning(request, 'Invalid Form, Please Try Again')

	else:
		form = FamilyDoctorForm()

	return render_to_response('RadiologySys/updateFamilyDoctor.html', {'form': form}, context)

def update_user(request):
	context = RequestContext(request)

	try:
		user = request.session.get('updateUser')
		if user == "":
			user = None
	except:
		user = None

	if request.method == 'POST':
		try:
			user = request.POST['user']
			request.session['updateUser'] = user
			userInst = Users.objects.get(user_name=user)
			person = userInst.person_id
			form1 = UserForm(instance=userInst)
			form2 = PersonForm(instance=person)
			return render_to_response('RadiologySys/updateUser.html', {'user': user, 'form1': form1, 'form2': form2}, context)

		except:
			userInst = Users.objects.get(user_name=user)
			person = userInst.person_id
			form1 = UserForm(request.POST, instance=userInst)
			form2 = PersonForm(request.POST, instance=person)

			if form1.is_valid() and form2.is_valid():
				form1.save()
				form2.save()
				messages.success(request, 'User Updated')
				request.session['updateUser'] = None
				return render_to_response('RadiologySys/updateUser.html', {'user': user, 'form1': form1, 'form2': form2}, context) 

			else:
				messages.warning(request, 'Invalid Form, Please Try Again')
				request.session['updateUser'] = None
				return render_to_response('RadiologySys/updateUser.html', {'user': user, 'form1': form1, 'form2': form2}, context) 

	else:
		form1 = UserForm()
		form2 = PersonForm()
		request.session['updateUser'] = None
		return render_to_response('RadiologySys/updateUser.html', {'user': user, 'form1': form1, 'form2': form2}, context)

def new_user(request):
	context = RequestContext(request)

	if request.method == 'POST':
		form1 = UserForm(request.POST)
		form2 = PersonForm(request.POST)

		if form1.is_valid() and form2.is_valid():

			form2.save()

			person_id = form2.cleaned_data['person_id']
			person = Persons.objects.get(person_id=person_id)
			usr = form1.save(commit=False)
			today = date.today()
			usr.date_registered = today
			usr.person_id = person

			usr.save()
			

			messages.success(request, 'New User Added')
			return render_to_response('RadiologySys/newUser.html', {'form1': form1, 'form2': form2}, context) 

		else:
			messages.warning(request, 'Invalid Form, Please Try Again')

	else:
		form1 = UserForm()
		form2 = PersonForm()

	return render_to_response('RadiologySys/newUser.html', {'form1': form1, 'form2': form2}, context)

def change_info(request):
	context = RequestContext(request)

	username = request.session.get('username')
	person = (Users.objects.get(user_name=username)).person_id
	# person = Persons.objects.get(person_id = userPerson_id)
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
		newFirst = request.POST['first']
		newLast = request.POST['last']
		newAddress = request.POST['address']
		newEmail = request.POST['email']
		newPhone = request.POST['phone']

		if newFirst != "":
			person.first_name = newFirst
			firstName = person.first_name
			request.session['first_name'] = firstName
		if newLast != "":
			person.last_name = newLast
			lastName = person.last_name
			request.session['last_name'] = lastName
		if newAddress != "":
			person.address = newAddress
			address = person.address
			request.session['address'] = address
		if newEmail != "":
			person.email = newEmail
			email = person.email
			request.session['email'] = email
		if newPhone != "":
			person.phone = newPhone
			phone = person.phone
			request.session['phone'] = phone

		person.save()
		messages.success(request, 'Info Updated')

		return render_to_response('RadiologySys/changeInfo.html', {'firstName': firstName, 'lastName': lastName, 'address': address, 'email': email, 'phone': phone}, context)

	else:
		return render_to_response('RadiologySys/changeInfo.html', {'firstName': firstName, 'lastName': lastName, 'address': address, 'email': email, 'phone': phone}, context)
	
def change_pass(request):
    context = RequestContext(request)
    username = request.session.get('username')
    password = request.session.get('password')

    if request.method == 'POST':

        pass1 = request.POST['password1']
        pass2 = request.POST['password2']

        if pass1 == pass2 and pass1 != "" and pass1 != password:

            user = Users.objects.get(user_name=username)
            user.password = pass1
            user.save()
            request.session['password'] = pass1
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

		

def user_login(request):
	context = RequestContext(request)

	if request.method == 'POST':

	   	# get username and password
		username = request.POST['username']
		password = request.POST['password']
		prev = {"username": username, "password": password}

		request.session['username'] = username
		request.session['password'] = password

	    # user returned if valid
		user = myLogin(username, password)

		if user:
			#store class
			request.session['class'] = user.get_classType_display()

			return HttpResponseRedirect('/home/')

		else:
			print("Invalid login credentials: {0}, {1}".format(username, password))
			messages.warning(request, "Invalid Login, Please Try Again")
			return render_to_response('RadiologySys/login.html', prev, context)
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

	    # Save previous parameters to display
	    prev = {"diagnosis": diagnosis,
	            "time_start": tstart,
	            "time_end": tend}

	    # Ensures valid time frame
	    if tstart > tend:
	        messages.warning(request, "Error: Start date after end date")
	        return render_to_response('RadiologySys/report.html', prev, context)
	    else:
	        cursor = connection.cursor()
	        cursor.execute('''Select    p.first_name, p.address, p.phone, r.test_date
	                            from    RadiologySys_persons p, RadiologySys_radiology_record r 
	                            where   p.person_id = r.patient_id_id and
	                                    r.test_type = %s and
	                                    r.test_date >= %s and
	                                    r.test_date <= %s''', [diagnosis, tstart, tend])
	        result = []
	        # Convert query to presentable format
	        for row in cursor.fetchall():
	            for i in range(len(row)):
	                result.append(row[i])

	        prev['results'] = result
	        messages.success(request, " ")
	        return render_to_response('RadiologySys/report.html', prev, context)

	else:
	    return render_to_response('RadiologySys/report.html', {}, context)


def myLogin(username, password):
	try:
		user = Users.objects.get(user_name=username)
	except:
		return None

	if user.password == password:
		return user
	else: 
		return None