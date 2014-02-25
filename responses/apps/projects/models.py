from django.db import models
from model_utils import Choices


class Project(models.Model):
    STATUS_CHOICES = Choices(
        (1, 'CREATED', 'Created and not launched'),
        (2, 'RUNNING', 'TASK RUNNING'),
        (3, 'FINISHED', 'Finished'),
    )
    urls = models.TextField(help_text="List of urls you want to check (one each line)", null=False)
    results = models.TextField(null=True)
    email = models.EmailField(help_text="We'll send you an e-mail when the task is finished", null=False)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=STATUS_CHOICES.CREATED)
    created = models.DateTimeField(auto_now_add=True)
    ended = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return "%s-%s" % (self.pk, self.email)


class RequestHeaders(models.Model):
    name = models.CharField(max_length=250)
    value = models.CharField(max_length=250)
    project = models.ForeignKey('Project', related_name='requests_headers')
