from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'resumes.views.view_resumes', name='view'),
    url(r'^download/csv$', 'resumes.views.export_csv', name='as_csv'),
]
