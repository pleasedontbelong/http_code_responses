from django.conf.urls import patterns, url
from django.contrib import admin
from django.views.generic import TemplateView

from projects import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^result/(?P<pk>[\d]+)$',
        views.ProjectResultsView.as_view(),
        name='project_results'),

    url(r'^success$',
        TemplateView.as_view(template_name='project/success.jinja2'),
        name='project_success'),

    url(r'^$',
        views.ProjectCreateView.as_view(),
        name='project_create'),
)
