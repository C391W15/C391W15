from django.shortcuts import *
from RadiologySys.models import *
from django.shortcuts import redirect
from django.contrib import messages
from RadiologySys.forms import *
from datetime import date
from django.db import connection

#homepage view
def index(request):
	context = RequestContext(request)

	#store class in order to show proper modules
	myClass = request.session.get('class')

	return render_to_response('RadiologySys/home.html', {'class': myClass}, context)

# the user documentation/help section
def help(request):
	context = RequestContext(request)
	return render_to_response('RadiologySys/help.html', {}, context)

#upload images and attach them to a radiology record
def upload_images(request):
	context = RequestContext(request)

	if request.method == 'POST':
		form = ImagesForm(request.POST)
		
		if form.is_valid():			

			# get the three image sizes
			thumb = form.cleaned_data['thumbnail']
			reg = form.cleaned_data['regular_size']
			full = form.cleaned_data['full_size']

			# ensure none of the image sizes are missing
			if thumb != None and reg != None and full != None:
				form.save()
				# success
				messages.success(request, 'Images Uploaded')
				return render_to_response('RadiologySys/uploadImages.html', {'form': form}, context) 
			else:
				# missing an image 
				messages.warning(request, 'Ensure all image sizes are filled in')

		else:
			# something is wrong with input
			messages.warning(request, 'Invalid Form, Please Try Again')

	else:
		form = ImagesForm()

	return render_to_response('RadiologySys/uploadImages.html', {'form': form}, context)

# uplaod a radiology record
def upload_record(request):
	context = RequestContext(request)

	if request.method == 'POST':
		form = RadiologyForm(request.POST)
		
		if form.is_valid():			

			# the following code is a slight workaround in order to make sure the only options given 
			# are the proper ones (ie. you can only select doctors from the doctors dropdown),
			# so we need to get persons from users
			rad = form.save(commit=False)

			doctor = form.cleaned_data['doctor_id']
			patient = form.cleaned_data['patient_id']
			radiologist = form.cleaned_data['radiologist_id']

			doctor = doctor.person_id
			patient = patient.person_id
			radiologist = radiologist.person_id

			rad.doctor_id = doctor
			rad.patient_id = patient
			rad.radiologist_id = radiologist

			rad.save()

			messages.success(request, 'Record Recorded')
			return render_to_response('RadiologySys/uploadRecord.html', {'form': form}, context) 

		else:
			messages.warning(request, 'Invalid Form, Please Try Again')

	else:
		form = RadiologyForm()

	return render_to_response('RadiologySys/uploadRecord.html', {'form': form}, context)

# user managment menu
def user_managment(request):
	context = RequestContext(request)
	request.session['updateUser'] = None
	return render_to_response('RadiologySys/userManagment.html', {}, context)

# update family doctor table
def update_family_doctor(request):
	context = RequestContext(request)

	if request.method == 'POST':
		form = FamilyDoctorForm(request.POST)
		
		if form.is_valid():			

			# this is the same workaround as the radiology record, where we need to ensure
			# the dropdowns only give certain options
			doctor = form.cleaned_data['doctor_id']
			patient = form.cleaned_data['patient_id']

			doctor = doctor.person_id
			patient = patient.person_id

			relationship = Family_doctor(doctor_id=doctor, patient_id=patient)
			relationship.save()

			messages.success(request, 'New Doctor/Patient Relationship Added')
			return render_to_response('RadiologySys/updateFamilyDoctor.html', {'form': form}, context) 

		else:
			messages.warning(request, 'Invalid Form, Please Try Again')

	else:
		form = FamilyDoctorForm()

	return render_to_response('RadiologySys/updateFamilyDoctor.html', {'form': form}, context)

# this updates a user that already exists
def update_user(request):
	context = RequestContext(request)

	# this try block is making it so that when you search for someone and the page reloads it will give the results
	# and if the search was incorrect, it reshows the search with the error message
	try:
		user = request.session.get('updateUser')
		if user == "":
			user = None
	except:
		user = None

	if request.method == 'POST':
		try:
			# see if they were searching or entering a form
			user = request.POST['user']
			try:
				# if the user was searching try and get the username
				userInst = Users.objects.get(user_name=user)
			except:
				# otherwise they were looking for a user that doesn't exist
				messages.warning(request, 'User doesn\'t exist')
				request.session['updateUser'] = None
				return render_to_response('RadiologySys/updateUser.html', {}, context)

			# show the form with that users info already showing
			request.session['updateUser'] = user
			person = userInst.person_id
			form1 = UserForm(instance=userInst)
			form2 = PersonForm(instance=person)
			return render_to_response('RadiologySys/updateUser.html', {'user': user, 'form1': form1, 'form2': form2}, context)

		except:
			# try to get the user
			try:
				userInst = Users.objects.get(user_name=user)
			except:
				messages.warning(request, 'User doesn\'t exist')
				request.session['updateUser'] = None
				return render_to_response('RadiologySys/updateUser.html', {}, context)
			# valid person, display their info
			person = userInst.person_id
			form1 = UserForm(request.POST, instance=userInst)
			form2 = PersonForm(request.POST, instance=person)

			if form1.is_valid() and form2.is_valid():
				# update was valid
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

# create a new user
def new_user(request):
	context = RequestContext(request)

	if request.method == 'POST':
		form1 = UserForm(request.POST)
		form2 = PersonForm(request.POST)

		if form1.is_valid() and form2.is_valid():

			form2.save()

			# set the date registered to current date
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

# change users info
def change_info(request):
	context = RequestContext(request)
	# get the users current info
	username = request.session.get('username')
	person = (Users.objects.get(user_name=username)).person_id
	firstName = person.first_name
	lastName = person.last_name
	address = person.address
	email = person.email
	phone = person.phone
	# set the info
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

		# if a field isn't blank, update that field in the database 
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

# change the users password	
def change_pass(request):
    context = RequestContext(request)
    # get username and password
    username = request.session.get('username')
    password = request.session.get('password')

    if request.method == 'POST':
    	# get the input
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']

        # if the passwords match and aren't blank and new password isn't the users current password
        if pass1 == pass2 and pass1 != "" and pass1 != password:

        	#update the password in the database
            user = Users.objects.get(user_name=username)
            user.password = pass1
            user.save()
            request.session['password'] = pass1
            messages.success(request, 'Password updated')

            return render_to_response('RadiologySys/changePass.html', {}, context)
        # if the password entered is the current password
        elif pass1 == password:
            messages.warning(request, "Password is the same, Please Try Again")
            return render_to_response('RadiologySys/changePass.html', {}, context)
        # error, passwords don't match
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
	    elif tstart == "" or tend == "" or diagnosis == "":
	    	messages.warning(request, "Error: Ensure all fields are filled in")
	    	return render_to_response('RadiologySys/report.html', prev, context)
	    else:
	        cursor = connection.cursor()
	        cursor.execute('''Select    p.first_name, p.address, p.phone, min(r.test_date)
	                            from    RadiologySys_persons p, RadiologySys_radiology_record r 
	                            where   p.person_id = r.patient_id_id and
	                                    r.test_type = %s and
	                                    r.test_date >= %s and
	                                    r.test_date <= %s
                                group by p.first_name, p.address, p.phone''', [diagnosis, tstart, tend])
	        result = []
	        # Convert query to presentable format
	        for row in cursor.fetchall():
	            for i in range(len(row)):
	                result.append(row[i])

	        if len(result) == 0:
	        	messages.warning(request, "No results returned. Please try again")
	        	return render_to_response('RadiologySys/report.html', prev, context)
	        else:
	        	prev['results'] = result
	        	messages.success(request, " ")
	        	return render_to_response('RadiologySys/report.html', prev, context)

	else:
	    return render_to_response('RadiologySys/report.html', {}, context)

def analysis(request):
	context = RequestContext(request)

	if request.method == 'POST':
		try:
			time = request.POST['time']
		except:
			time = 'all'
		try:
			name = request.POST['name']
		except:
			name = None
		try:
			tp = request.POST['type']
		except:
			tp = None

		prev = {'time': time,
				'name': name,
				'type': tp}

		sortString = "" # No selection (default)
		selectString = "Select count(image_id)"
		queryString = " From temp"
		groupString = " Group by "

		if time != "all": # Time was selected
			sortString = time # Time is either week/month/year
			selectString += ", year"
			groupString += "year"
			if time == "week":
				selectString += ", week"
				groupString += ", week"
			elif time == "month":
				selectString += ", month"
				groupString += ", month"

			if name == "True" and tp == "True": # All 3 were selected
				sortString += ", patient and type "
				selectString += ", person_id, test_type"
				groupString += ", person_id, test_type"
			elif name == "True" or tp == "True": # One other selection was made (Type or patient)
				sortString += " and "
				groupString += ", "

		if name == None and tp == "True": # Type was selected
			sortString += "type"
			selectString += ", test_type"
			groupString += "test_type"
		elif name == "True" and tp == None: # Patient was selected
			sortString += "patient"
			selectString += ", person_id"
			groupString += "person_id"
		elif name == "True" and tp == "True" and time == "all": # Only Patient and Type selected
			sortString += "patient and type"
			selectString += ", person_id, test_type"
			groupString += "person_id, test_type"

		print(sortString)
		if name == None and tp == None and time == "all":
			messages.success(request, "Displaying Total number of images ever taken")
		else:
			messages.success(request, "Displaying Total number of images, sorted by " + sortString)

		queryString = selectString + queryString + groupString
		print(queryString)

		cursor = connection.cursor()

		cursor.execute('''Create temporary table if not exists temp as (
							Select person_id, week, month, year, test_type, image_id 
							From RadiologySys_persons p
								Inner Join RadiologySys_radiology_record r
									on r.patient_id_id = p.person_id
								Inner Join RadiologySys_time t
									on t.time_id = r.time_id_id
								Inner Join RadiologySys_Pacs_images i
									on i.record_id_id = r.record_id)''')
		cursor.execute(queryString)

		result = []

		for row in cursor.fetchall():
			for i in range(len(row)):
				result.append(row[i])

		print(result)

		return render_to_response('RadiologySys/analysis.html', prev, context)
	else:
		return render_to_response('RadiologySys/analysis.html', {'time': 'all'}, context)

def myLogin(username, password):
	try:
		user = Users.objects.get(user_name=username)
	except:
		return None

	if user.password == password:
		return user
	else: 
		return None
