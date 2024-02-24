import logging

from django.core import mail

logger = logging.getLogger(__name__)


def send_mail(subject: str, html_message: str, from_email: str, recipient_list: list[str]) -> bool:
    return mail.send_mail(
        subject=subject,
        message=None,
        html_message=html_message,
        from_email=from_email,
        recipient_list=recipient_list,
    )
