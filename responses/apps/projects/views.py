from django.core.urlresolvers import reverse
from django.conf import settings

from responses.core.generic import CreateView, DetailView

from .models import Project
from .forms import ProjectCreateForm
from .tasks import check_urls_task


class ProjectCreateView(CreateView):
    """
    Creates a new organization
    """
    template_name = 'project/create_form.jinja2'
    model = Project
    form_class = ProjectCreateForm

    def get_success_url(self):
        check_urls_task.delay(self.object.pk)
        return reverse('project_create')

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(*args, **kwargs)
        context['MAX_URL_CHECK'] = settings.MAX_URL_CHECK
        return context


class ProjectResultsView(DetailView):
    template_name = 'project/detail.jinja2'
    model = Project
