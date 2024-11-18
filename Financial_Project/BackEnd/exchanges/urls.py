from django.urls import path
from . import views

app_name = 'exchanges'
urlpatterns = [
    path('', views.index, name='index'),
    path('bankmap/', views.bankmap, name='bankmap'),
    path('test/', views.test, name='test'),
]
