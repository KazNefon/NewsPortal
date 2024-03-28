from django.shortcuts import render, get_object_or_404
from .models import News
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from .models import Article
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
