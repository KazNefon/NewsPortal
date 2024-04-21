from django.core.mail import send_mail
from .models import Article, User, Category
from django.utils import timezone
from datetime import timedelta

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
