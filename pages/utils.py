# Django
from django.conf import settings
from django.core.mail import get_connection
from django.core.mail.message import EmailMultiAlternatives


def send_mail(self, subject, message, recipient_list, from_email=None, reply_to=None, **kwargs):
    if not from_email:
        if hasattr(settings, "WAGTAILADMIN_NOTIFICATION_FROM_EMAIL"):
            from_email = settings.WAGTAILADMIN_NOTIFICATION_FROM_EMAIL
        elif hasattr(settings, "DEFAULT_FROM_EMAIL"):
            from_email = settings.DEFAULT_FROM_EMAIL
        else:
            from_email = "webmaster@localhost"

    connection = kwargs.get("connection", False) or get_connection(
        username=kwargs.get("auth_user", None),
        password=kwargs.get("auth_password", None),
        fail_silently=kwargs.get("fail_silently", None),
    )
    multi_alt_kwargs = {
        "connection": connection,
        "headers": {
            "Auto-Submitted": "auto-generated",
        },
    }
    mail = EmailMultiAlternatives(subject, message, from_email, recipient_list, reply_to=reply_to, **multi_alt_kwargs)
    html_message = kwargs.get("html_message", None)
    if html_message:
        mail.attach_alternative(html_message, "text/html")

    return mail.send()
