from django.db import models
from django.contrib.auth.models import User

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

######################################################
# Model representing a person
# Contains basic contact information
######################################################
class Persons(models.Model):
	person_id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=24)
	last_name = models.CharField(max_length=24)
	address = models.CharField(max_length=128)
	email = models.CharField(max_length=128, unique=True)
	phone = models.CharField(max_length=10)

	def __str__(self):
		return self.first_name

######################################################
# Model representing a user
# Contains user information such as username/password 
# and priviledges
######################################################
class Users(models.Model):
	CLASSES = (('a','Admin'), ('p', 'Patient'), ('d', 'Doctor'), ('r', 'Radiologist'))
	user_name = models.CharField(max_length=24, primary_key=True, unique=True)
	password = models.CharField(max_length=24)
	classType = models.CharField(max_length=1, choices=CLASSES)
	person_id = models.ForeignKey(Persons)
	date_registered = models.DateField()

	def __str__(self):
		return self.user_name

######################################################
# Model representing the relationship between patient 
# and doctor
######################################################
class Family_doctor(models.Model):
	doctor_id = models.ForeignKey(Persons, related_name = 'person_idDoc')
	patient_id = models.ForeignKey(Persons, related_name = 'person_idPat')

######################################################
# Model representing time
# Used to index the time a record is tested
######################################################
class Time(models.Model):
	weeks = [(i,i) for i in range(1, 53)]
	months = [(i,i) for i in range(1, 13)]

	time_id = models.AutoField(primary_key=True)
	week = models.IntegerField(choices=weeks)
	month = models.IntegerField(choices=months)
	year = models.IntegerField()

	def __str__(self):
		return self.time_id

######################################################
# Model representing a record
# Contains basic information about an entered record
# Time is indexed based on test_date not prescribing date
######################################################
class Radiology_record(models.Model):
	record_id = models.AutoField(primary_key = True)
	patient_id = models.ForeignKey(Persons, related_name = 'person_idPatRec')
	doctor_id = models.ForeignKey(Persons, related_name = 'person_idDocRec')
	radiologist_id = models.ForeignKey(Persons, related_name = 'person_idRadRec')
	test_type = models.CharField(max_length=24)
	prescribing_date = models.DateField()
	test_date = models.DateField()
	time_id = models.ForeignKey(Time, editable = False)
	diagnosis = models.CharField(max_length=128)
	description = models.CharField(max_length=1024)

	# Function used to dynamically assign a time_id to the test_date provided by record
	def save(self):
		dt = self.test_date
		yr = dt.year
		mth = dt.month
		wk = dt.isocalendar()[1]

		self.time_id = Time.objects.get(week = wk, month = mth, year = yr)
		super(Radiology_record, self).save()

	def __str__(self):
		return str(self.record_id)

######################################################
# Model representing an uploaded image
# Fields available for multiple sizes of images
######################################################
class Pacs_images(models.Model):
	record_id = models.ForeignKey(Radiology_record, related_name = 'record_idPic')
	image_id = models.AutoField(primary_key = True)
	thumbnail = models.ImageField(upload_to = 'thumbnails', blank=True)
	regular_size = models.ImageField(upload_to = 'regular_size', blank=True)
	full_size = models.ImageField(upload_to = 'full_size', blank=True)

	def __str__(self):
		return str(self.image_id)

