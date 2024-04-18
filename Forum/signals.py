from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, Notification, Like
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import User


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:

            if instance.parent is not None and instance.parent.user != instance.user:  # Avoid self-notification
                Notification.objects.create(
                    notification_type=Notification.REPLY,
                    to_user=instance.parent.user,
                    from_user=instance.user,
                    thread=instance.thread,
                    comment=instance,
                    is_read=False
                )


