from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import send_mail_func
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail_func.apply_async(args=[instance.email])
