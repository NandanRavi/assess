from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from users.models import CustomUser
from .models import Like

@receiver(post_save, sender=CustomUser)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance, message="A new user has registered!")


@receiver(post_save, sender=Like)
def notify_like(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.liked_user,
            message=f"{instance.user.name} liked your profile."
        )
