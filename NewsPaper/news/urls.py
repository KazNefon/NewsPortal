from django.urls import path
from .views import news_list, news_detail
from .views import news_search
from .views import NewsCreateView
from .views import NewsUpdateView
from .views import NewsDeleteView
from .views import ArticleCreateView
from .views import ArticleUpdateView
from .views import ArticleDeleteView
from allauth.account.views import LoginView, LogoutView, SignupView, PasswordChangeView


urlpatterns = [
    path('news/', news_list, name='news_list'),
    path('news/<int:news_id>/', news_detail, name='news_detail'),
    path('news/search/', news_search, name='news_search'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('accounts/login/', LoginView.as_view(), name='account_login'),
    path('accounts/logout/', LogoutView.as_view(), name='account_logout'),
    path('accounts/signup/', SignupView.as_view(), name='account_signup'),
    path('accounts/password/change/', PasswordChangeView.as_view(), name='account_change_password'),
    path('category/<int:category_id>/subscribe/', subscribe, name='subscribe'),
]
