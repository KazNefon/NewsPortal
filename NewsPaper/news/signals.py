from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Article
from django.urls import reverse


@receiver(post_save, sender=Article)
def article_created(sender, instance, created, **kwargs):
    if created:
        subscribers = instance.category.subscribers.all()
        for subscriber in subscribers:
            send_mail(
                subject=instance.title,
                message=f'Здравствуй, {subscriber.username}. Новая статья в твоём любимом разделе! {instance.text[:50]}...',
                from_email='kaz5kaz@mail.ru',
                recipient_list=[subscriber.email],
                fail_silently=False,
            )


def send_welcome_email(user):
    subject = 'Добро пожаловать на News Portal!'
    message = f'Здравствуйте, {user.username}!\nСпасибо за регистрацию на нашем сайте. Пожалуйста, активируйте свой аккаунт, перейдя по следующей ссылке: http://127.0.0.1:8000 {reverse("activation_view", args=[user.activation_key])}'
    from_email = 'kaz5kaz@mail.ru'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=Article)
def send_notification_to_subscribers(sender, instance, created, **kwargs):
    if created:
        subscribers = instance.category.subscribers.all()
        for subscriber in subscribers:
            send_mail(
                subject=f'Новая статья в категории {instance.category.name}',
                message=f'Привет {subscriber.username}, проверьте новую статью: {instance.title}. Краткое содержание: {instance.text[:50]}...',
                from_email='kaz5kaz@mail.ru',
                recipient_list=[subscriber.email],
                fail_silently=False,
            )
