from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^secrets$', views.secrets),
    url(r'^add_secret$', views.add_secret),
    url(r'^most_popular$', views.most_popular),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^like/(?P<id>\d+)$', views.like),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^logout$', views.logout),
]
