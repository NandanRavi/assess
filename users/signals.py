from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from .tasks import send_mail_func

@receiver(post_save, sender=CustomUser)
def send_welcome_email_signal(sender, instance, created, **kwargs):
    if created:
        send_mail_func.delay(instance.email)
