from django.shortcuts import render, get_object_or_404
from .models import News

def news_list(request):
    news_items = News.objects.all().order_by('-pub_date')
    return render(request, 'news_list.html', {'news_items': news_items})

def news_detail(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news_detail.html', {'news_item': news_item})
