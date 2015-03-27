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
                       url(r'^home/', views.index, name='index'),
                       url(r'^report/', views.report, name='report'),
                       url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
                       url(r'^changePass/', views.change_pass, name='Change Password'),
                       url(r'^changeInfo/', views.change_info, name='Change Info'),

                       )
