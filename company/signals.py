import django.dispatch
from django.core.mail import send_mail as mail
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

company_email_changed = django.dispatch.Signal(providing_args=["company"])
company_contact_person_email_changed = django.dispatch.Signal(providing_args=["company_contact_person"])


@receiver(company_email_changed)
def send_mail_to_company(sender, **kwargs):
    send_email(kwargs["company"].email)


@receiver(company_contact_person_email_changed)
def send_mail_to_company_contact_person(sender, **kwargs):
    send_email(kwargs["company_contact_person"].email)


def get_recipient(email):
    return email if not settings.DEBUG else settings.EMAIL_HOST_USER


def send_email(email):
    recipient = get_recipient(email)
    logger.info("Sending email to: %s" % recipient.split("@")[0])
    message = render_to_string("message_to_company.txt", {'email': email})
    mail(subject="Informacja o przetwarzaniu panstwa danych", message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[recipient])