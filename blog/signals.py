from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Post

@receiver(post_save, sender=Post)
def send_post_published_notification(sender, instance, created, **kwargs):
    """
    Send notification when a post is published
    """
    if instance.status == 'published' and not created:
        # In a real application, you might want to send emails to subscribers
        # For now, we'll just print to console
        print(f"Post '{instance.title}' has been published!")
        
        # Example email sending (uncomment and configure if you want to use)
        # subject = f'New Post Published: {instance.title}'
        # message = f'A new post "{instance.title}" has been published. Check it out!'
        # from_email = settings.DEFAULT_FROM_EMAIL
        # recipient_list = ['subscribers@example.com']
        # send_mail(subject, message, from_email, recipient_list)