from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'membership.views.dashboard', name='dashboard'),
    url(r'^search$', 'membership.views.search', name='search'),
]