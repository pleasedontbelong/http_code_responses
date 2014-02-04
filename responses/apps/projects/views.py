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


class ProjectResultsView(DetailView):
    template_name = 'project/detail.jinja2'
    model = Project
