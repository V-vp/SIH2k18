from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$',views.index,name='index'),
    #url(r'^list/$',views.list,name='list'),
    url(r'^rp/$',views.ranked_panchayats,name='list'),
    url(r'^pd/$',views.panchayat_details,name='panchayat_details'),
    url(r'^panchayat_list/$',views.panchayat_list,name='panchayat_list'),
    url(r'^panchayat/(?P<pk>\d+)/$', views.panchayat, name='panchayat'),
    url(r'^vd/$',views.vd,name='vd'),
]
