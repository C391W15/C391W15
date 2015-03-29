from RadiologySys.models import *
from django import forms
from django.utils.translation import ugettext_lazy as _

class UserForm(forms.ModelForm):
	class Meta:
		model = Users
		fields = ['user_name', 'password', 'classType']
		

class PersonForm(forms.ModelForm):
	class Meta:
		model = Persons
		fields = ['first_name', 'last_name', 'person_id', 'address', 'email', 'phone']

class FamilyDoctorForm(forms.Form):
	doctor_id = forms.ModelChoiceField(queryset=Users.objects.filter(classType='d'))
	patient_id = forms.ModelChoiceField(queryset=Users.objects.filter(classType='p'))

class RadiologyForm(forms.ModelForm):
	doctor_id = forms.ModelChoiceField(queryset=Users.objects.filter(classType='d'))
	patient_id = forms.ModelChoiceField(queryset=Users.objects.filter(classType='p'))
	radiologist_id = forms.ModelChoiceField(queryset=Users.objects.filter(classType='r'))

	class Meta:
		model = Radiology_record
		exclude = ['radiologist_id', 'doctor_id', 'patient_id']
		labels = {
            'prescribing_date': _('Prescribing Date (YYYY-MM-DD)'),
            'test_date': _('Test Date (YYYY-MM-DD)'),
        }

class ImagesForm(forms.ModelForm):
	class Meta:
		model = Pacs_images
		fields = '__all__'