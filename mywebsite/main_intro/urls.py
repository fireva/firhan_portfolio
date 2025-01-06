
from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page (redirects to About Me)
    path('about/', views.about, name='about'),  # About Me page
    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
]