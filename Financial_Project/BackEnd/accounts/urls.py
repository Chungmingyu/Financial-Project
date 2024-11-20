# accounts/urls.py
from django.urls import path
from .views import RegisterView, UserProfileView, UserUpdateView
from dj_rest_auth.views import LoginView, LogoutView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserProfileView.as_view(), name='user'),
    path('user/update/', UserUpdateView.as_view(), name='user-update'),

]
