# accounts/urls.py
from django.urls import path
from .views import RegisterView, UserProfileView, UserUpdateView, UserUpdateView, BoardListCreateView, BoardDetailView, UserDepositListCreateView, UserDepositDeleteView
from dj_rest_auth.views import LoginView, LogoutView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


urlpatterns = [
    # 유저 기본 뷰
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserProfileView.as_view(), name='user'),
    path('user/update/', UserUpdateView.as_view(), name='user-update'),
    # 게시판 관련 뷰
    path('boards/', BoardListCreateView.as_view(), name='board-list-create'),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name='board-detail'),
]
