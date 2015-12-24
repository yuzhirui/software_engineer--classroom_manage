# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout
from classroom import views 
import settings

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    # Examples:
    # url(r'^$', 'classroommanage.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^submit', views.submit),
    url(r'^bui/$', views.bui),
    url(r'^buil/$', views.buil),
    url(r'^inq/$',views.inq),
    url(r'^flo/$',views.flo), 
    url(r'^$', views.home),
    url(R'^task/$', views.task),
    url(r'^admindisplay/$', views.admindisplay),
    url(r'^details/$', views.orderdetails),
    url(r'^orders/$', views.order_room),
    url(r'^updateinform/$', views.updateinform),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$', views.home),
    url(r'^register/$', views.register),
    url(r'^changepw/$', views.changepwd),
    url(r'^login/$', views.login),
    url(r'^logout/$', logout),
    url(r'^contact/$', views.contact),
    url(r'^inquire/$', views.inquire),
    url(r'^appointment/$', views.appointment),
    url(r'^forget/$', views.forget),
#    url(r'^test/$', views.test),
)
