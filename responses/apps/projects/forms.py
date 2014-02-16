from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .models import Project

from base.forms import SimpleFormHelper


class ProjectCreateForm(forms.ModelForm):
    """ Create a project form """
    class Meta:
        model = Project
        fields = ['urls', 'email']

    def __init__(self, *args, **kwargs):
        self.helper = SimpleFormHelper("Check Status")
        self.helper.form_class = 'form-group'
        self.helper.attrs = {'role': 'form'}
        super(ProjectCreateForm, self).__init__(*args, **kwargs)

    def clean_urls(self):
        self.cleaned_data['urls'] = self.cleaned_data['urls'].strip()
        if self.cleaned_data['urls'].count('\r') > settings.MAX_URL_CHECK:
            raise forms.ValidationError(_('You can not check more than %d urls') % settings.MAX_URL_CHECK)
        return self.cleaned_data['urls']
