from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Article

@receiver(post_save, sender=Article)
def article_created(sender, instance, created, **kwargs):
    if created:
        subscribers = instance.category.subscribers.all()
        for subscriber in subscribers:
            send_mail(
                subject=instance.title,
                message=f'Здравствуй, {subscriber.username}. Новая статья в твоём любимом разделе! {instance.text[:50]}...',
                from_email='from@example.com',
                recipient_list=[subscriber.email],
                fail_silently=False,
            )
