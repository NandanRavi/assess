from celery import shared_task
from django.core.mail import send_mail
from assessmentProject import settings



@shared_task(bind=True)
def send_mail_func(self, email):
    mail_subject = 'Welcome to Our Platform'
    message = 'Thank you for registering. Enjoy our platform!'
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
