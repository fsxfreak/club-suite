from django.conf.urls import url, include
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm  # easy registration
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete#password reset
from django.conf.urls.static import static
from django.conf import settings


import django.contrib.auth as auth

from . import views

urlpatterns = [
    url(r'^about', views.About.as_view(), name='about'),
    url(r'^dashboard', views.Dashboard.as_view(), name='dashboard'),
    url(r'^club/create', views.ClubCreate.as_view(), name='club_create'),
    url(r'^club/search', views.ClubSearch.as_view(), name='club_search'),
    url(r'^club/roster', views.ClubRoster.as_view(), name='club_roster'),
    url(r'^club/(?P<club_id>[0-9]+)/$', views.ClubView.as_view(), name='club_view'),
    url(r'^account', views.Account.as_view(), name='account'),

    #password reset

      url(r'^reset-password/$', password_reset, {'template_name': 'registration/password_reset_form.html', 'post_reset_redirect': 'suite:password_reset_done', 'email_template_name': 'registration/password_reset_email.html'}, name='reset_password'),

    url(r'^reset-password/done/$', password_reset_done, {'template_name': 'registration/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'template_name': 'registration/password_reset_confirm.html', 'post_reset_redirect': 'suite:password_reset_complete'}, name='password_reset_confirm'),

    url(r'^reset-password/complete/$', password_reset_complete,{'template_name': 'registration/reset_password_complete.html'}, name='password_reset_complete'),

    # user registration
    url('^', include('django.contrib.auth.urls')),
    url('^$', auth.views.login, name='login'),
    #url('^$', views.view_index, name='login'),

    url(r'^register$', views.RegistrationView.as_view(), name='register'),
    url(r'^register/done$', auth.views.password_reset_done, {
            'template_name': 'registration/initial_done.html',
        }, name='register_done'),
    url(r'^register/password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth.views.password_reset_confirm, {
            'template_name': 'registration/initial_confirm.html',
            'post_reset_redirect': 'suite:register_complete',
        }, name='register_confirm'),
    url(r'^register/complete/$', auth.views.password_reset_complete, {
            'template_name': 'registration/initial_complete.html',
        }, name='register_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
