import os 
import datetime

def populate():
	addPerson('Aaron', 'Tse', '111 Fake Street', 'akt@ualberta.ca', '1231231313')
	addPerson('Cody', 'Ingram', '123 Fake Street', 'cdingram@ualberta.ca', '0980989898')
	addPerson('Ondra', 'Chan', '133 Fake Street', 'ondra@ualberta.ca', '4564564646')
	addPerson('Chris', 'Li', '144 Fake Street', 'lisheung@ualberta.ca', '3453453535')

	addUser('akt', 'bar', 'a', '1', datetime.date(2000, 10, 10))
	addUser('cdingram', 'foo', 'p', '2', datetime.date(2010, 5, 1))
	addUser('ondra', 'bar', 'd', '3', datetime.date(2009, 4, 1))
	addUser('chris', 'foo', 'r', '4', datetime.date(2014, 3,20))

	addRecord('2', '3', '4', 'Cancer', datetime.date(2005, 5, 10), datetime.date(2005, 5, 11), 'Safe', 'No issues found')
	addRecord('2', '3', '4', 'Cancer', datetime.date(2006, 3, 3), datetime.date(2006, 3, 3), 'Infected', 'Recommend immediate action')
	addRecord('2', '3', '4', 'AIDS', datetime.date(2006, 6, 15), datetime.date(2006, 6, 15), 'Infected', 'Patient was found with the AIDS virus')
	addRecord('2', '3', '4', 'Sore Throat', datetime.date(2010, 4, 1), datetime.date(2010, 4, 8), 'Safe', 'No issues found')
	addRecord('2', '3', '4', 'Broken Leg', datetime.date(2015, 5, 3), datetime.date(2015, 5, 3), 'Broken', 'Patient requires cane for the rest of his life')

	for i in range(1,13):
		for j in range (1, 53):
			for k in range(1990, 2016):
				if abs(i*4 - j) < 4:
					t = Time(week = i, month = j, year = k)
					t.save()
					print(t.time_id, t.week, t.month, t.year)

def addPerson(first, last, address, email, phone):
	p = Persons(first_name = first, last_name = last, address = address, email = email, phone = phone)
	p.save()
	print(p)

def addUser(user, pass, class, id, registered):
	u = Users(user_name = user, password = pass, classType = class, person_id = id,  date_registered = registered)
	u.save()
	print(u)

def addRecord(patient, doctor, radiologist, test_type, prescribe, test, diagnosis, description):
	r = Radiology_record(patient_id = patient, doctor_id = doctor, radiologist_id = radiologist, test_type = test_type, prescribe_date = prescribe, test_date = test, diagnosis = diagnosis, description = description)
	r.save()
	print(r)

if __name__ == '__main__':
    print("Populating time fields...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'radiology.settings')
    # from django.db import models
    from RadiologySys.models import *
    populate()