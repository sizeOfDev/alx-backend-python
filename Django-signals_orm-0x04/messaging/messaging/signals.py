from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from models import Message, Notification


@receiver(post_save, sender=Message)
def send_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            read=False
        )
        print(f"Notification created for {instance.receiver} regarding new message from {instance.sender}.")

@receiver(post_save, sender=Notification)
def notification_saved(sender, instance, created, **kwargs):
    if created:
        print(f"Notification for {instance.user} regarding message {instance.message.id} has been saved.")
    else:
        print(f"Notification for {instance.user} regarding message {instance.message.id} has been updated.")
