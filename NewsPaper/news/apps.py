from django.apps import AppConfig
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'


class YourAppConfig(AppConfig):
    name = 'NewsPaper'

    def ready(self):
        import NewsPaper.signals


class MyAppConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        from .tasks import weekly_newsletter
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Запуск задачи каждую неделю
        scheduler.add_job(
            weekly_newsletter,
            'interval',
            weeks=1,
            name='send_weekly_newsletter',
            jobstore='default',
        )
        scheduler.start()
