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
