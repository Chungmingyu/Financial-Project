from django.urls import path
from . import views

urlpatterns = [
    path('', views.fetch_google_news, name='fetch_google_news'),
]
