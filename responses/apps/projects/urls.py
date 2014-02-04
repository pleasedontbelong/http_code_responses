from django.conf.urls import patterns, url
from django.contrib import admin

from projects import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^/result/(?P<pk>[\d]+)$',
        views.ProjectResultsView.as_view(),
        name='project_results'),

    url(r'^$',
        views.ProjectCreateView.as_view(),
        name='project_create'),
)
