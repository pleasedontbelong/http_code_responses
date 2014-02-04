from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class SimpleFormHelper(FormHelper):
    def __init__(self, submit_text=False, *args, **kwargs):
        super(SimpleFormHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.form_class = 'crispy_form'
        self.help_text_inline = True
        self.error_text_inline = False

        if not submit_text:
            submit_text = _('Save')
        self.add_input(Submit('submit', submit_text))
