from celery.task.base import task

from .models import Project

import requests

USER_AGENT = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"


@task
def check_urls_task(project_id):
    project = Project.objects.get(pk=project_id)
    for url in project.urls.split('\n'):
        try:
            request = requests.head(url, headers={'User-Agent': USER_AGENT})
            print url
            print request.status_code
            #prints the int of the status code. Find more at httpstatusrappers.com :)
        except:
            print "failed to connect"
