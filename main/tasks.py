
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from main.models import Subscription
from users.models import User


@shared_task
def send_emails(emails, subject, message, from_email):

    send_mail(subject,
              message,
              from_email,
              recipient_list=emails,
              fail_silently=False
              )




