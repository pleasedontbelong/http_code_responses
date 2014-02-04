import logging

from django.core import mail
from django.core.exceptions import ImproperlyConfigured
from django.template import loader
from django.utils import translation
from django.db.models.loading import cache
from django.conf import settings
from django.template import Context


email_logger = logging.getLogger('emails')


def send_template_email(recipients, title_template, body_template, context, language=None):
    """Sends e-mail using templating system"""

    site_name = getattr(settings, 'SITE_NAME', 'Please define settings.SITE_NAME')
    domain = getattr(settings, 'SITE_URL', None)

    if domain is None:
        Site = cache.get_model('sites', 'Site')
        current_site = Site.objects.get_current()
        site_name = current_site.name
        domain = current_site.domain

    context.update({
        'site_name': site_name,
        'site_domain': domain
    })

    if language is not None:
        translation.activate(language)

    mail_title_template = loader.get_template(title_template)
    mail_body_template = loader.get_template(body_template)
    title = mail_title_template.render(Context(context)).strip()
    body = mail_body_template.render(Context(context))

    try:
        email_from = getattr(settings, 'DEFAULT_FROM_EMAIL')
    except AttributeError:
        raise ImproperlyConfigured('DEFAULT_FROM_EMAIL setting needed for sending e-mails')

    mail.send_mail(title, body, email_from, recipients)

    if language is not None:
        translation.deactivate()

    email_logger.info(u"Email (%s) sent to %s\nTitle: %s\n%s\n\n" % (language, recipients, title, body))
