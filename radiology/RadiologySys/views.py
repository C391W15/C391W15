from django.shortcuts import *
from RadiologySys.models import *
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection

# Create your views here.
def index(request):
    context = RequestContext(request)
    return render_to_response('RadiologySys/home.html', {}, context)


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

            user = Users.objects.get(user_name=username)
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

        # get username and password
        username = request.POST['username']
        password = request.POST['password']
        prev = {"username": username,
                "password": password}

        request.session['username'] = username
        request.session['password'] = password

        # user returned if valid
        user = myLogin(username, password)

        if user:
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
            cursor.close()
            return render_to_response('RadiologySys/report.html', prev, context)

    else:
        return render_to_response('RadiologySys/report.html', {}, context)


def myLogin(username, password):
    # Handle user not in database
    try:
        user = Users.objects.get(user_name=username)
    except ObjectDoesNotExist:
        return None

    if user.password == password:
        return user
    else:
        return None




