from django.conf.urls import url
from resumes import views

urlpatterns = [
    url(r'^$', views.view_resumes, name='view'),
    url(r'^download/csv$', views.export_csv, name='as_csv'),
]
