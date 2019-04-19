from django.conf.urls import url 
from . import views

urlpatterns = [ 
    url(r'^list/$', views.list_videos, name='list_videos'),
    url(r'^list/search/$', views.search_videos, name='search_videos'),
    url(r'^view/$', views.view_video, name='view_video'),
]