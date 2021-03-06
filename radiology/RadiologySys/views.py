from django.shortcuts import *
from RadiologySys.models import *
from django.shortcuts import redirect
from django.contrib import messages
from RadiologySys.forms import *
from datetime import date
from django.db import connection
import calendar

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
		form = ImagesForm(request.POST, request.FILES)
		
		if form.is_valid():			
			# get all three images
			thumb = form.cleaned_data['thumbnail']
			reg = form.cleaned_data['regular_size']
			full = form.cleaned_data['full_size']
			#print(thumb, reg, full)
			# ensure no image is missing
			if thumb != None and reg != None and full != None:
				# success
				f = form.save(commit = False)
				f.thumbnail = thumb
				f.regular_size = reg
				f.full_size = full
				f.save()
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
			#invalid form
			messages.warning(request, 'Invalid Form, Please Try Again')

	else:
		# not a post, show form
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
			request.session['myID'] = (user.person_id).person_id

			return HttpResponseRedirect('/home/')

		else:
			print("Invalid login credentials: {0}, {1}".format(username, password))
			messages.warning(request, "Invalid Login, Please Try Again")
			return render_to_response('RadiologySys/login.html', prev, context)
	else:
	    return render_to_response('RadiologySys/login.html', {}, context)


#############################################################################################################
# This module allows the user to find a list of records given a test type and a time frame
# The results from the executed query is stored in a list and then added to the dictionary of variables accessible 
# by the html template
# The query searches based on test date
#############################################################################################################

def report(request):
	context = RequestContext(request)

	if request.method == 'POST':

	    # Get diagnosis and time frame
	    diagnosis = request.POST['diagnosis']
	    tstart = request.POST['time_start']
	    tend = request.POST['time_end']

		# Dictionary used to store values accessible by html template
	    # Contains the previously entered parameters
	    prev = {"diagnosis": diagnosis,
	            "time_start": tstart,
	            "time_end": tend}

	   	# Error handling
	    # Ensures valid time frame
	    if tstart > tend:
	        messages.warning(request, "Error: Start date after end date")
	        return render_to_response('RadiologySys/report.html', prev, context)
	   	# Ensures valid fields
	    elif tstart == "" or tend == "" or diagnosis == "":
	    	messages.warning(request, "Error: Ensure all fields are filled in")
	    	return render_to_response('RadiologySys/report.html', prev, context)
	    else:
	    # Execute query
	        cursor = connection.cursor()
	        cursor.execute('''Select    p.first_name, p.address, p.phone, min(r.test_date)
	                            from    RadiologySys_persons p, RadiologySys_radiology_record r 
	                            where   p.person_id = r.patient_id_id and
	                                    r.test_type = %s and
	                                    r.test_date >= %s and
	                                    r.test_date <= %s
                                group by p.first_name, p.address, p.phone''', [diagnosis, tstart, tend])
	        result = []
	        # Append query to list for displaying in html template
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

	else: # HttpGET request
	    return render_to_response('RadiologySys/report.html', {}, context)

#############################################################################################################
# This module allows the user to select up to 3 options to sort by: Test type, Patient name, and a Time frame
# Test type and Patient name are represented as checkboxes and Time frame is represented as radiobuttons where
# "All" is the default and is equivalent to no Time frame selected
# This module dynamically builds a query string depending on the options selected and returns the query that is
# executed. The query is stored in a list and then added to the variables dictionary to view in an html template
#############################################################################################################

def analysis(request):
	context = RequestContext(request)

	if request.method == 'POST':

		# Determine which options were selected
		##########################################################################################
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

		# Dictionary used to store values accessible by html template
		# Contains the previous selected options
		prev = {'time': time,
				'name': name,
				'type': tp}
		##########################################################################################
		# Section where query string is built
		# sortString is the string built for displaying the "sorted by" message in template
		# query string is broken up into 3 parts and concatenated together at the end
		##########################################################################################
		sortString = "" # No selection (default)

		selectString = "Select count(image_id)"
		queryString = " From temp"
		groupString = " Group by "
		length = 1 # Variable to track number of columns needed (dynamic depending on solution)

		flag = (False, "") # Variable to track whether time is represented as year or year + week or year + month
		if time != "all": # Time was selected
			sortString = time 
			selectString += ", year"
			groupString += "year"
			length += 1
			if time == "week":
				selectString += ", week"
				groupString += ", week"
				length += 1
				flag = (True, "week")
			elif time == "month":
				selectString += ", month"
				groupString += ", month"
				length += 1
				flag = (True, "month")

			if name == "True" and tp == "True": # All 3 were selected
				sortString += ", patient and type "
				selectString += ", person_id, test_type"
				groupString += ", person_id, test_type"
				length += 2
			elif name == "True" or tp == "True": # One other selection was made (Type or patient)
				sortString += " and "
				groupString += ", "

		if name == None and tp == "True": # Type was selected
			sortString += "type"
			selectString += ", test_type"
			groupString += "test_type"
			length += 1
		elif name == "True" and tp == None: # Patient was selected
			sortString += "patient"
			selectString += ", person_id"
			groupString += "person_id"
			length += 1
		elif name == "True" and tp == "True" and time == "all": # Only Patient and Type selected
			sortString += "patient and type"
			selectString += ", person_id, test_type"
			groupString += "person_id, test_type"
			length += 2

		# Creating message for display
		if name == None and tp == None and time == "all":
			messages.success(request, "Displaying Total number of images ever taken")
		else:
			messages.success(request, "Displaying Total number of images, sorted by " + sortString)

		# Concatenating queryString
		if groupString == " Group by ":
			queryString = selectString + queryString
		else:
			queryString = selectString + queryString + groupString

		##########################################################################################
		# The cursor first creates a temporary table containing person_id, week, month, year, test_type and image_id
		# The cursor then executes the queryString which extracts the necessary info from the temp table
		# and groups it based on the chosen parameters
		# Query is parsed and then inserted into a list which is added to the dictinoary of variables
		# accessible by the html template
		# The query is run based on "test_date"
		##########################################################################################

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

		result = [] # List to store query results

		for row in cursor.fetchall():
			for i in range(len(row)):
				if flag[0]: # if Week or Month is selected
					if i == 2: # roww[2] represents "week" or "month" in the query (based on my queryString)
						if flag[1] == "week":
							temp = "week " + str(row[i])
							result.insert(0, temp)
						else:
							result.insert(0, calendar.month_name[row[i]])
					else:
						result.insert(0, row[i])
				else:
					result.insert(0, row[i])

		cursor.close()

		if len(result) == 0:
			# Error handling
			messages.warning(request, "No images in the database")
			return render_to_response('RadiologySys/analysis.html', prev, context)
		else:
			# Add values to dicionary for parsing in html template
			prev['results'] = result 
			prev['length'] = length
			return render_to_response('RadiologySys/analysis.html', prev, context)

	else: # Request was a GET request
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


def search(request):
	context = RequestContext(request)
	# Requird for user security
	c = request.session.get('class')
	myID = request.session.get('myID')

	if request.method == 'POST':

		# Get keywords and time frame
		key_words = request.POST['key_words']
		tstart = request.POST['time_start']
		tend = request.POST['time_end']

		# Split up the keywords into singular varchars
		ks = key_words.split(" ")

		# Save previous parameters to display
		prev = {"key_words": ks,
				"time_start": tstart,
				"time_end": tend}
		
		# Ensures valid time frame
		if tstart > tend:
			messages.warning(request, "Error: Start date after end date")
			return render_to_response('RadiologySys/search.html', prev, context)

		elif (tstart == '' and tend != ''):
			messages.warning(request, "Error: Please enter both dates")
			return render_to_response('RadiologySys/search.html', prev, context)

		elif (tstart != '' and tend == ''):
			messages.warning(request, "Error: Please enter both dates")
			return render_to_response('RadiologySys/search.html', prev, context)

		else:
			result = []

			if (tstart == '' and tend == ''):
				if c == 'Admin':
					for k in ks:

						cursor = connection.cursor()
						cursor.execute('''SELECT Distinct	p.first_name,
															d.first_name,
															i.first_name,
															r.test_type,
															r.prescribing_date,
															r.test_date,
															r.diagnosis,
															r.description
										from 	(RadiologySys_persons p, RadiologySys_persons d, RadiologySys_persons i, RadiologySys_radiology_record r)
										where  	(p.person_id = r.patient_id_id and
												d.person_id = r.doctor_id_id and
												i.person_id = r.radiologist_id_id) or

												p.first_name LIKE %s or
												p.last_name LIKE %s or
												
												d.first_name LIKE %s or
												d.last_name LIKE %s or
												
												i.first_name LIKE %s or
												i.last_name LIKE %s or

												r.test_type LIKE %s or
												r.diagnosis LIKE %s or
												r.description LIKE %s ''', [k, k, k, k, k, k, '%' + k + '%', '%' + k + '%', '%' + k + '%'])

						for row in cursor.fetchall():
							for i in range(len(row)):
								result.append(row[i])

				if c == 'Doctor':
					print("Test")
					cursor = connection.cursor()
					cursor.execute('''SELECT Distinct p.first_name
									FROM RadiologySys_persons p, radiologysys_family_doctor f, RadiologySys_radiology_record r
									WHERE f.doctor_id_id = r.doctor_id_id and
										p.person_id = f.patient_id_id
									''')
					patients = []
					for row in cursor.fetchall():
						for i in range(len(row)):
							patients.append(row[i])
					print(patients)

					for k in ks:
						print("Test 2")
						cursor = connection.cursor()
						cursor.execute('''SELECT Distinct	p.first_name,
															d.first_name,
															i.first_name,
															r.test_type,
															r.prescribing_date,
															r.test_date,
															r.diagnosis,
															r.description
										from 	(RadiologySys_persons p, RadiologySys_persons d, RadiologySys_persons i, RadiologySys_radiology_record r)
										where  	(p.person_id = r.patient_id_id and
												d.person_id = r.doctor_id_id and
												i.person_id = r.radiologist_id_id) or

												p.first_name LIKE %s or
												p.last_name LIKE %s or
												
												d.first_name LIKE %s or
												d.last_name LIKE %s or
												
												i.first_name LIKE %s or
												i.last_name LIKE %s or

												r.test_type LIKE %s or
												r.diagnosis LIKE %s or
												r.description LIKE %s 

										''', [k, k, k, k, k, k, '%' + k + '%', '%' + k + '%', '%' + k + '%'])
						for row in cursor.fetchall():
							if row[0] in patients:
								for i in range(len(row)):
									result.append(row[i])

						print(result)

				if c == 'Radiologist':
					for k in ks:

						cursor = connection.cursor()
						cursor.execute('''SELECT Distinct	p.first_name,
															d.first_name,
															i.first_name,
															r.test_type,
															r.prescribing_date,
															r.test_date,
															r.diagnosis,
															r.description
										from 	(RadiologySys_persons p, RadiologySys_persons d, RadiologySys_persons i, RadiologySys_radiology_record r)
										where  	r.radiologist_id_id = %s and
												(p.person_id = r.patient_id_id and
												d.person_id = r.doctor_id_id and
												i.person_id = r.radiologist_id_id) or

												p.first_name LIKE %s or
												p.last_name LIKE %s or
												
												d.first_name LIKE %s or
												d.last_name LIKE %s or
												
												i.first_name LIKE %s or
												i.last_name LIKE %s or

												r.test_type LIKE %s or
												r.diagnosis LIKE %s or
												r.description LIKE %s ''', [myID, k, k, k, k, k, k, '%' + k + '%', '%' + k + '%', '%' + k + '%'])

						for row in cursor.fetchall():
							for i in range(len(row)):
								result.append(row[i])


				if c == 'Patient':
					for k in ks:

						cursor = connection.cursor()
						cursor.execute('''SELECT Distinct	p.first_name,
															d.first_name,
															i.first_name,
															r.test_type,
															r.prescribing_date,
															r.test_date,
															r.diagnosis,
															r.description
										from 	(RadiologySys_persons p, RadiologySys_persons d, RadiologySys_persons i, RadiologySys_radiology_record r)
										where  	r.patient_id_id = %s and
												(p.person_id = r.patient_id_id and
												d.person_id = r.doctor_id_id and
												i.person_id = r.radiologist_id_id) or

												p.first_name LIKE %s or
												p.last_name LIKE %s or
												
												d.first_name LIKE %s or
												d.last_name LIKE %s or
												
												i.first_name LIKE %s or
												i.last_name LIKE %s or

												r.test_type LIKE %s or
												r.diagnosis LIKE %s or
												r.description LIKE %s ''', [myID, k, k, k, k, k, k, '%' + k + '%', '%' + k + '%', '%' + k + '%'])

						for row in cursor.fetchall():
							for i in range(len(row)):
								result.append(row[i])

			else:
				if c == 'Admin':
					for k in ks:

						cursor = connection.cursor()
						cursor.execute('''SELECT Distinct	p.first_name,
															d.first_name,
															i.first_name,
															r.test_type,
															r.prescribing_date,
															r.test_date,
															r.diagnosis,
															r.description
										from 	(RadiologySys_persons p, RadiologySys_persons d, RadiologySys_persons i, RadiologySys_radiology_record r)
										where  	(p.person_id = r.patient_id_id and
												d.person_id = r.doctor_id_id and
												i.person_id = r.radiologist_id_id and 
												r.test_date >= %s and
	                                    		r.test_date <= %s) or

												p.first_name LIKE %s or
												p.last_name LIKE %s or
												
												d.first_name LIKE %s or
												d.last_name LIKE %s or
												
												i.first_name LIKE %s or
												i.last_name LIKE %s or

												r.test_type LIKE %s or
												r.diagnosis LIKE %s or
												r.description LIKE %s ''', [tstart, tend, k, k, k, k, k, k, '%' + k + '%', '%' + k + '%', '%' + k + '%'])

						for row in cursor.fetchall():
							for i in range(len(row)):
								result.append(row[i])

				if c == 'Doctor':
					cursor = connection.cursor()
					cursor.execute('''SELECT Distinct p.first_name
									FROM RadiologySys_persons p, radiologysys_family_doctor d, RadiologySys_radiology_record r
									WHERE f.doctor_id_id = r.doctor_id_id and
										p.person_id = f.patient_id_id
									''')
					patients = []
					for row in cursor.fetchall():
						for i in range(len(row)):
							patients.append(row[i])

					for k in ks:

						cursor = connection.cursor()
						cursor.execute('''SELECT Distinct	p.first_name,
															d.first_name,
															i.first_name,
															r.test_type,
															r.prescribing_date,
															r.test_date,
															r.diagnosis,
															r.description
										from 	(RadiologySys_persons p, RadiologySys_persons d, RadiologySys_persons i, RadiologySys_radiology_record r)
										where  	(p.person_id = r.patient_id_id and
												d.person_id = r.doctor_id_id and
												i.person_id = r.radiologist_id_id and
												r.test_date >= %s and
	                                    		r.test_date <= %s) or

												p.first_name LIKE %s or
												p.last_name LIKE %s or
												
												d.first_name LIKE %s or
												d.last_name LIKE %s or
												
												i.first_name LIKE %s or
												i.last_name LIKE %s or

												r.test_type LIKE %s or
												r.diagnosis LIKE %s or
												r.description LIKE %s ''', [tstart, tend, k, k, k, k, k, k, '%' + k + '%', '%' + k + '%', '%' + k + '%'])

						for row in cursor.fetchall():
							for i in range(len(row)):
								if (i%8 == 0) and (row[i] in patients):
									result.append(row[i])
								else:
									i+=8

				if c == 'Radiologist':
					for k in ks:

						cursor = connection.cursor()
						cursor.execute('''SELECT Distinct	p.first_name,
															d.first_name,
															i.first_name,
															r.test_type,
															r.prescribing_date,
															r.test_date,
															r.diagnosis,
															r.description
										from 	(RadiologySys_persons p, RadiologySys_persons d, RadiologySys_persons i, RadiologySys_radiology_record r)
										where  	(p.person_id = r.patient_id_id and
												d.person_id = r.doctor_id_id and
												i.person_id = r.radiologist_id_id and
												r.test_date >= %s and
	                                    		r.test_date <= %s) or

												p.first_name LIKE %s or
												p.last_name LIKE %s or
												
												d.first_name LIKE %s or
												d.last_name LIKE %s or
												
												i.first_name LIKE %s or
												i.last_name LIKE %s or

												r.test_type LIKE %s or
												r.diagnosis LIKE %s or
												r.description LIKE %s ''', [tstart, tend, k, k, k, k, k, k, '%' + k + '%', '%' + k + '%', '%' + k + '%'])

						for row in cursor.fetchall():
							for i in range(len(row)):
								result.append(row[i])


				if c == 'Patient':
					for k in ks:

						cursor = connection.cursor()
						cursor.execute('''SELECT Distinct	p.first_name,
															d.first_name,
															i.first_name,
															r.test_type,
															r.prescribing_date,
															r.test_date,
															r.diagnosis,
															r.description
										from 	(RadiologySys_persons p, RadiologySys_persons d, RadiologySys_persons i, RadiologySys_radiology_record r)
										where  	r.patient_id_id = %s and
												(p.person_id = r.patient_id_id and
												d.person_id = r.doctor_id_id and
												i.person_id = r.radiologist_id_id and
												r.test_date >= %s and
	                                   		 	r.test_date <= %s) or

												p.first_name LIKE %s or
												p.last_name LIKE %s or
												
												d.first_name LIKE %s or
												d.last_name LIKE %s or
												
												i.first_name LIKE %s or
												i.last_name LIKE %s or

												r.test_type LIKE %s or
												r.diagnosis LIKE %s or
												r.description LIKE %s ''', [myID, tstart, tend k, k, k, k, k, k, '%' + k + '%', '%' + k + '%', '%' + k + '%'])

						for row in cursor.fetchall():
							for i in range(len(row)):
								result.append(row[i])


			prev['results'] = result
			messages.success(request, " ")
			return render_to_response('RadiologySys/search.html', prev, context)

	else:
		return render_to_response('RadiologySys/search.html', {}, context)

