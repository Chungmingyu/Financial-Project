from django.urls import path
from . import views
app_name = 'bankmap'

urlpatterns = [
    path('', views.index, name="index")
]
