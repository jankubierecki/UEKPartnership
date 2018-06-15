import django.dispatch
from django.core.mail import send_mail as mail
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

company_email_changed = django.dispatch.Signal(providing_args=["company"])
company_contact_person_email_changed = django.dispatch.Signal(providing_args=["company_contact_person"])


@receiver(company_email_changed)
def send_mail_to_company(sender, **kwargs):
    company = kwargs["company"]
    send_email(company.email)
    company.privacy_email_date_send = timezone.now()
    company.save(update_fields=["privacy_email_date_send"])


@receiver(company_contact_person_email_changed)
def send_mail_to_company_contact_person(sender, **kwargs):
    company_contact_person = kwargs["company_contact_person"]
    send_email(company_contact_person.email)
    company_contact_person.privacy_email_date_send = timezone.now()
    company_contact_person.save(update_fields=["privacy_email_date_send"])


def get_recipient(email):
    return email if not settings.DEBUG else settings.EMAIL_HOST_USER


def send_email(email):
    recipient = get_recipient(email)
    logger.info("Sending email to: %s" % recipient.split("@")[0])
    message = render_to_string("message_to_company.txt", {'email': email})
    mail(subject="Informacja o przetwarzaniu panstwa danych", message=message, from_email=settings.EMAIL_HOST_USER,
         recipient_list=[recipient])
