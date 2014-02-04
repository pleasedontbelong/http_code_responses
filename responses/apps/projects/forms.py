from django import forms

from .models import Project

from base.forms import SimpleFormHelper


class ProjectCreateForm(forms.ModelForm):
    """ Create a project form """
    class Meta:
        model = Project
        fields = ['urls', 'email']

    def __init__(self, *args, **kwargs):
        self.helper = SimpleFormHelper("Create")
        super(ProjectCreateForm, self).__init__(*args, **kwargs)
