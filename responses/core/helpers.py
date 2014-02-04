from django.contrib.staticfiles.storage import staticfiles_storage
from django.template import Context
from django.conf import settings

from jinja2 import contextfunction
from jingo import register
from crispy_forms import utils


@register.function
def debug():
    return settings.TEMPLATE_DEBUG


@register.function
@contextfunction
def crispy(context, form, helper):
    """
    Renders the form using crispy_forms
    """
    return utils.render_crispy_form(form, helper, context)


@register.function
@contextfunction
def crispy_field(context, field, form, form_style="", **kwargs):
    return utils.render_field(field, form, form_style, Context(), **kwargs)


@register.function
def static(path):
    return staticfiles_storage.url(path)
