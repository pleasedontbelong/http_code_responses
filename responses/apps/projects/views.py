from django.core.urlresolvers import reverse

from responses.core.generic import CreateView, DetailView

from .models import Project
from .forms import ProjectCreateForm


class ProjectCreateView(CreateView):
    """
    Creates a new organization
    """
    template_name = 'project/create_form.jinja2'
    model = Project
    form_class = ProjectCreateForm

    def get_success_url(self):
        # Return the reversed success url.
        return reverse('project_create')


class ProjectResultsView(DetailView):
    template_name = 'project/detail.jinja2'
    model = Project
