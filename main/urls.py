"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from main import views

app_name = "main"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("q/", views.queries, name="queries"),
    path("articles/", views.articles, name="queries"),
    path("hashtags/", views.hashtags, name="hashtags"),
    path("keywords/", views.keywords, name="keywords"),
    path("queries/", views.queries, name="queries"),
    path("query_runs/", views.query_runs, name="query_runs"),
    path("results/", views.results, name="results"),
    path("twitter_imports/", views.twitter_imports, name="twitter_imports"),
    path("register/", views.register, name="register"),
    
]
