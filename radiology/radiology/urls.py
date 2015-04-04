from django.conf.urls import patterns, include, url
from django.contrib import admin
from RadiologySys import views

urlpatterns = patterns('',
   # Examples:
   # url(r'^$', 'radiology.views.home', name='home'),
   # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^$', views.user_login, name='login'),
	url(r'^login', views.user_login, name='login'),
	url(r'^home/', views.index, name='home'),
	url(r'^changePass/', views.change_pass, name='Change Password'),
	url(r'^changeInfo/', views.change_info, name='Change Info'),
	url(r'^userManagment/', views.user_managment, name='User Managment'),
	url(r'^newUser/', views.new_user, name='New User'),
	url(r'^updateUser/', views.update_user, name='Update User'),
	url(r'^report/', views.report, name='report'),
	url(r'^familyDoctorUpdate/', views.update_family_doctor, name='Update Family Doctor'),
	url(r'^uploadRecord/', views.upload_record, name='Upload Radiology Record'),
	url(r'^uploadImages/', views.upload_images, name='Upload Images'),
	url(r'^help/', views.help, name='help'),
	url(r'^analysis/', views.analysis, name='Data Analysis'),
)