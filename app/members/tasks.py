# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.core.mail import send_mail

from config.celery import app


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@app.task(bind=False)
def my_send_email():
    send_mail(
        'Subject here',
        'Here is the message.',
        'folivoradev@gmail.com',
        ['folivoradev@gmail.com'],
        fail_silently=False,
    )
    return 1
