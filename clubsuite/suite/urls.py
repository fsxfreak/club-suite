from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^about', views.Index.as_view(), name='about'),
    url(r'^dashboard', views.Index.as_view(), name='dashboard'),
    url(r'^create_club', views.Index.as_view(), name='club'),
    url(r'^create_event', views.Index.as_view(), name='event'),
    url(r'^account', views.Index.as_view(), name='account'),
    url(r'^club_view', views.Index.as_view(), name='club_view'),
]
