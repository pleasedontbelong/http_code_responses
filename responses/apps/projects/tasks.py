from django.utils import timezone
from celery.task.base import task

from .models import Project

import requests

USER_AGENT = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"


@task
def check_urls_task(project_id):
    project = Project.objects.get(pk=project_id)
    project.status = Project.STATUS_CHOICES.RUNNING
    project.save(update_fields=['status'])
    out = ""
    for url in project.urls.split('\n'):
        url = url.rstrip()
        try:
            request = requests.head(url, headers={'User-Agent': USER_AGENT})
            out += "%s;%s\n" % (url, request.status_code)
        except:
            out += "%s;%s\n" % (url, "failed to connect")
    project.status = Project.STATUS_CHOICES.FINISHED
    project.ended = timezone.now()
    project.results = out
    project.save(update_fields=['status', 'ended', 'results'])
