from django.core.mail import send_mail
from .models import Article, User, Category
from django.utils import timezone
from datetime import timedelta
from celery import shared_task
from django.utils.timezone import now, timedelta


def weekly_newsletter():
    last_week = timezone.now() - timedelta(days=7)
    categories = Category.objects.all()

    for category in categories:
        articles = Article.objects.filter(category=category, created_at__gte=last_week)
        if articles.exists():
            subscribers = category.subscribers.all()
            subject = f'Новые статьи в категории {category.name}'
            message = f'За последнюю неделю в категории "{category.name}" появились новые статьи:\n\n'
            message += "\n".join([article.title for article in articles])
            recipient_list = [subscriber.email for subscriber in subscribers]

            send_mail(subject, message, 'from@example.com', recipient_list)


@shared_task
def send_notification_email(user_email, message):
    send_mail(
        'Новая статья доступна',
        message,
        'kaz5kaz@mail.com',
        [user_email],
        fail_silently=False,
    )


@shared_task
def send_weekly_news_email():
    last_week = timezone.now() - timedelta(days=7)
    articles = Article.objects.filter(created_at__gte=last_week)
    if articles.exists():
        for user in User.objects.all():
            subject = 'Еженедельный дайджест новостей'
            message = 'Привет! Вот новости за последнюю неделю:\n\n' + '\n'.join(article.title for article in articles)
            send_mail(subject, message, 'kaz5kaz@mail.com', [user.email])