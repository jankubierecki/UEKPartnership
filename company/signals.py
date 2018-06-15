import django.dispatch
from django.core.mail import send_mail as mail
from django.db import transaction
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings
import logging
from django.utils import timezone
from company import models


logger = logging.getLogger(__name__)

company_email_changed = django.dispatch.Signal(providing_args=["company"])
company_contact_person_email_changed = django.dispatch.Signal(providing_args=["company_contact_person"])


def email_notification_time(email, time):
    models.EmailInformedUsers.objects.create(email=email, created_at=time)


def is_email_notified(email):
    return models.EmailInformedUsers.objects.filter(email=email).exists()


@receiver(company_email_changed)
def send_mail_to_company(sender, **kwargs):
    now = timezone.now()
    company = kwargs["company"]
    if send_email(company.email, now):
        company.privacy_email_date_send = now
        company.save(update_fields=["privacy_email_date_send"])


@receiver(company_contact_person_email_changed)
def send_mail_to_company_contact_person(sender, **kwargs):
    now = timezone.now()
    company_contact_person = kwargs["company_contact_person"]
    if send_email(company_contact_person.email, now):
        company_contact_person.privacy_email_date_send = now
        company_contact_person.save(update_fields=["privacy_email_date_send"])


def get_recipient(email):
    return email if not settings.DEBUG else settings.EMAIL_HOST_USER


def send_email(email, now):
    recipient = get_recipient(email)
    logger.info("Sending email to: %s" % recipient.split("@")[0])
    message = render_to_string("message_to_company.txt", {'email': email})
    with transaction.atomic():
        models.EmailInformedUsers.objects.select_for_update().all()
        if not is_email_notified(email):
            mail(subject="Informacja o przetwarzaniu panstwa danych", message=message,
                 from_email=settings.EMAIL_HOST_USER,
                 recipient_list=[recipient])
            email_notification_time(email, now)
            return True
    return False
