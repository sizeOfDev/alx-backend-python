from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from models import Message, Notification, MessageHistory


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



@receiver(pre_save, sender=Message)
def log_message_history(sender, instance, **kwargs):
    if instance.pk:
        old_message = Message.objects.get(pk=instance.pk)
        if old_message.content != instance.content:
            MessageHistory.objects.create(
                message=old_message,
                old_content=old_message.content,
                timestamp=old_message.timestamp
            )
            print(f"Message history logged for message {instance.pk}. Old content: {old_message.content}")
        else:
            print(f"No change in content for message {instance.pk}. No history logged.")
    else:
        print("Creating a new message, no history to log.") 

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    Notification.objects.filter(user=instance).delete()

    for message in Message.objects.filter(sender=instance) | Message.objects.filter(receiver=instance):
        MessageHistory.objects.filter(message=message).delete()
