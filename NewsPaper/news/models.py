from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.core.mail import send_mail


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        self.rating = 3 * sum(self.post_set.all().values_list('rating', flat=True))
        self.rating += sum(self.comment_set.all().values_list('rating', flat=True))
        self.rating += sum(self.post_set.all().values_list('comment__rating', flat=True))
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_categories')


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    TYPE_CHOICES = [
        ('article', 'Статья'),
        ('news', 'Новость'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.title


from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    given_name = models.CharField(max_length=255, verbose_name=_('Имя'))
    surname = models.CharField(max_length=255, verbose_name=_('Фамилия'))
    bio = models.TextField(blank=True, null=True, verbose_name=_('Биография'))
    image = models.ImageField(upload_to='uploads/', blank=True, null=True, verbose_name=_('Изображение'))

    def __str__(self):
        return f"{self.given_name} {self.surname}"

    class Meta:
        ordering = ['surname', 'given_name']


Group.objects.create(name='common')
Group.objects.create(name='authors')


@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    common_group = Group.objects.get(name='common')
    common_group.user_set.add(user)


@login_required
def become_author(request):
    authors_group = Group.objects.get(name='authors')
    authors_group.user_set.add(request.user)
    return redirect('some-view')


content_type = ContentType.objects.get_for_model(Post)
permission = Permission.objects.create(
    codename='can_publish',
    name='Can Publish Posts',
    content_type=content_type,
)

authors_group = Group.objects.get(name='authors')
authors_group.permissions.add(permission)


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Добро пожаловать на наш новостной портал!',
            f'Здравствуйте, {instance.username}! Спасибо за регистрацию.',
            'your-email@example.com',
            [instance.email],
            fail_silently=False,
        )