import django.dispatch
from django.db import transaction
from django.dispatch import receiver
from django.conf import settings
import logging
from django.utils import timezone
from company import models
from templated_email import send_templated_mail

logger = logging.getLogger(__name__)

company_email_changed = django.dispatch.Signal(providing_args=["company"])
company_contact_person_email_changed = django.dispatch.Signal(providing_args=["company_contact_person"])


def email_notification_time(email, time):
    models.EmailInformedUsers.objects.create(email=email, created_at=time)


@receiver(company_email_changed)
def send_mail_to_company(sender, **kwargs):
    now = timezone.now()
    company = kwargs["company"]
    company.privacy_email_date_send = mail_company(company.email, company.name, now)
    company.save(update_fields=["privacy_email_date_send"])


@receiver(company_contact_person_email_changed)
def send_mail_to_company_contact_person(sender, **kwargs):
    now = timezone.now()
    company_contact_person = kwargs["company_contact_person"]
    company_contact_person.privacy_email_date_send = mail_company_contact_person(company_contact_person.email,
                                                                                 company_contact_person.first_name, now)
    company_contact_person.save(update_fields=["privacy_email_date_send"])


def get_recipient(email):
    return email if settings.MAIL_NOTIFICATIONS else settings.EMAIL_HOST_USER


def mail_company(email, company_name, now):
    recipient = get_recipient(email)
    logger.info("Sending email to: %s" % recipient.split("@")[0])
    with transaction.atomic():
        models.EmailInformedUsers.objects.select_for_update().all()
        email_notified_list = models.EmailInformedUsers.objects.filter(email=email)
        if not email_notified_list:
            send_templated_mail(
                template_name='notification_company',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient],
                context={'company_name': company_name}
            )
            email_notification_time(email, now)
            return now
        else:
            return email_notified_list[0].created_at


def mail_company_contact_person(email, company_contact_person_name, now):
    recipient = get_recipient(email)
    logger.info("Sending email to: %s" % recipient.split("@")[0])
    with transaction.atomic():
        models.EmailInformedUsers.objects.select_for_update().all()
        email_notified_list = models.EmailInformedUsers.objects.filter(email=email)
        if not email_notified_list:
            send_templated_mail(
                template_name='notification_company_contact_person',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient],
                context={'company_contact_person_name': company_contact_person_name}
            )
            email_notification_time(email, now)
            return now
        else:
            return email_notified_list[0].created_at
