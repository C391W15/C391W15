from django.db import models
from django.contrib.auth.models import User

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# Create your models here.
class Persons(models.Model):
	person_id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=24)
	last_name = models.CharField(max_length=24)
	address = models.CharField(max_length=128)
	email = models.CharField(max_length=128, unique=True)
	phone = models.CharField(max_length=10)

	def __str__(self):
		return self.first_name

class Users(models.Model):
	CLASSES = (('a','Admin'), ('p', 'Patient'), ('d', 'Doctor'), ('r', 'Radiologist'))
	user_name = models.CharField(max_length=24, primary_key=True, unique=True)
	password = models.CharField(max_length=24)
	classType = models.CharField(max_length=1, choices=CLASSES)
	person_id = models.ForeignKey(Persons)
	date_registered = models.DateField()

	def __str__(self):
		return self.user_name

class Family_doctor(models.Model):
	doctor_id = models.ForeignKey(Persons, related_name = 'person_idDoc')
	patient_id = models.ForeignKey(Persons, related_name = 'person_idPat')

	# def __str__(self):
	# 	return self.family_doctor_text

class Time(models.Model):
	weeks = [(i,i) for i in range(1, 53)]
	months = [(i,i) for i in range(1, 13)]

	time_id = models.AutoField(primary_key=True)
	week = models.IntegerField(choices=weeks)
	month = models.IntegerField(choices=months)
	year = models.IntegerField()

	def __str__(self):
		return self.time_id

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

	def save(self):
		dt = self.test_date
		yr = dt.year
		mth = dt.month
		wk = dt.isocalendar()[1]

		self.time_id = Time.objects.get(week = wk, month = mth, year = yr)
		super(Radiology_record, self).save()

	def __str__(self):
		return str(self.record_id)

class Pacs_images(models.Model):
	record_id = models.ForeignKey(Radiology_record, related_name = 'record_idPic')
	image_id = models.AutoField(primary_key = True)
	thumbnail = models.ImageField(upload_to = 'thumbnails', blank=True)
	regular_size = models.ImageField(upload_to = 'regular_size', blank=True)
	full_size = models.ImageField(upload_to = 'full_size', blank=True)

	def __str__(self):
		return str(self.image_id)

