from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string


def send_mail(to, subject, template_name, context, from_email=None):
    """
    Sends an email to the supplied email address, using
    the template name and context.
    The template name should not include the file type; instead,
    it will search for .html and .txt versions of the template.
    NB both html and text versions are required.
    
    Can optionally specify a from_email, otherwise it will use
    CONTACT_EMAIL in the settings.
    """
    # Make to a list, if it isn't already
    if not isinstance(to, (list, tuple)):
        to = [to]

    if not from_email:
        from_email = settings.CONTACT_EMAIL

    context['domain'] = settings.DOMAIN
    context['contact_email'] = settings.CONTACT_EMAIL

    content = {}
    for content_format in ('txt', 'html'):
        content[content_format] = render_to_string('%s.%s' % (template_name,
                                                              content_format),
                                                   context)
    msg = EmailMultiAlternatives(subject,
                                 content['txt'],
                                 settings.DEFAULT_FROM_EMAIL,
                                 to)
    msg.attach_alternative(content['html'], "text/html")
    msg.send()
