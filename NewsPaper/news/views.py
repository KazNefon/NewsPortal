from django.shortcuts import render, get_object_or_404
from .models import News
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from .models import Article, Category
from .models import Profile
from allauth.account.forms import LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Post
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.utils.html import strip_tags


def news_list(request):
    def news_list(request):
        news_items = News.objects.all().order_by('-pub_date')
        paginator = Paginator(news_items, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'news_list.html', {'page_obj': page_obj})


def news_detail(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news_detail.html', {'news_item': news_item})


from django.db.models import Q


def news_search(request):
    query = request.GET.get('query', '')
    news_items = News.objects.filter(
        Q(title__icontains=query) |
        Q(author__icontains=query) |
        Q(pub_date__gt=query)
    ).order_by('-pub_date')
    paginator = Paginator(news_items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news_search.html', {'page_obj': page_obj, 'query': query})


class NewsCreateView(CreateView):
    model = News
    fields = ['title', 'content', 'pub_date']
    template_name = 'news_create.html'
    success_url = '/news/'


class NewsUpdateView(UpdateView):
    model = News
    fields = ['title', 'content', 'pub_date']
    template_name = 'news_edit.html'
    success_url = '/news/'


class NewsDeleteView(DeleteView):
    model = News
    template_name = 'news_delete.html'
    success_url = '/news/'


class ArticleCreateView(CreateView):
    model = Article
    fields = ['title', 'content', 'pub_date']
    template_name = 'article_create.html'
    success_url = '/articles/'


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ['title', 'content', 'pub_date']
    template_name = 'article_edit.html'
    success_url = '/articles/'


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = '/articles/'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['bio', 'location', 'birth_date']
    template_name = 'profile_edit.html'
    success_url = '/profile/'

    def get_object(self):
        return self.request.user.profile


def home(request):
    context = {
        'login_form': LoginForm()
    }
    return render(request, 'home.html', context)


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    fields = ['type', 'title', 'content', 'categories']
    template_name = 'post_form.html'
    success_url = '/posts/'
    permission_required = '.add_post'


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    fields = ['type', 'title', 'content', 'categories']
    template_name = 'post_form.html'
    success_url = '/posts/'
    permission_required = '.change_post'


@login_required
def subscribe(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.add(request.user)
    return redirect('category_detail', category_id=category_id)


def send_article_notification(article):
    subject = article.title
    for subscriber in article.category.subscribers.all():
        message = f"Здравствуй, {subscriber.username}. Новая статья в твоём любимом разделе! {article.text[:50]}..."
        html_message = f'<h1>{article.title}</h1><p>{article.text[:50]}...</p><a href="http://мойадресс.com/articles/{article.id}">Читать далее</a>'
        send_mail(subject, strip_tags(message), 'from@example.com', [subscriber.email], html_message=html_message)
