from django.conf.urls import patterns, include, url
from django.contrib import admin
from RadiologySys import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'radiology.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^', views.index, name='index'),
	url(r'^$', views.user_login, name='login'),
	#url(r'^RadiologySys/', include('RadiologySys.urls')),
	url(r'^home/', views.index, name='index'),

    
)
