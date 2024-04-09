from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, Notification, Like
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import User


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        # Notification for top-level comments to thread subscribers
        if instance.parent is None:
            subscribers = instance.thread.subscribers.exclude(id=instance.user.id)
            notifications = [
                Notification(
                    notification_type=Notification.COMMENT,
                    to_user=subscriber,
                    from_user=instance.user,
                    thread=instance.thread,
                    comment=instance,
                    is_read=False
                )
                for subscriber in subscribers
            ]
            Notification.objects.bulk_create(notifications)
        
        # Notification for replies directly to the commented user
        else:
            if instance.parent.user != instance.user:  # Avoid self-notification
                Notification.objects.create(
                    notification_type=Notification.REPLY,
                    to_user=instance.parent.user,
                    from_user=instance.user,
                    thread=instance.thread,
                    comment=instance,
                    is_read=False
                )


