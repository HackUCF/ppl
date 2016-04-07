from django.conf.urls import url
from membership import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^search$', views.search, name='search'),
    url(r'^update$', views.update, name='update'),
]
