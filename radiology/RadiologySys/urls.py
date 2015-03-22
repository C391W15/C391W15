from django.conf.urls import patterns, url
from RadiologySys import views

urlpatterns = patterns('', 
	url(r'^$', views.index, name='index'),
	url(r'^login/$', views.user_login, name='login'),
)