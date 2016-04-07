from django.conf.urls import include, url
from django.contrib import admin
import django.contrib.auth.views
import membership.views

urlpatterns = [
    url(r'^$', membership.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^login$', django.contrib.auth.views.login,
        {'template_name': 'auth/login.html'}, name='login'),
    url(r'^logout$', django.contrib.auth.views.logout,
        {'template_name': 'auth/logged_out.html'}, name='logout'),
    url(r'^membership/', include('membership.urls', namespace='membership')),
    url(r'^resumes/', include('resumes.urls', namespace='resumes'))
]
