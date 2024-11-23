# vue 랑 연동할거면하셈
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostListAPIView, PostCreateAPIView, ToggleLikeAPIView
from . import views

# router = DefaultRouter()
# router.register(r'posts', PostViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]

# boards/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', PostListAPIView.as_view(), name='post_list'),  # 게시글 목록
    path('<int:post_id>/', views.post_detail, name='post_detail'),  # 게시글 상세보기
    path('<int:post_id>/like/', ToggleLikeAPIView.as_view(),
         name='toggle-like'),  # 좋아요
    path('create/', PostCreateAPIView.as_view(), name='create_post'),
    path('delete/', views.delete_post, name='delete_post'),
    path('posts/<int:post_id>/comments/',
         views.comment_view, name='comment-view'),
    path('comments/<int:comment_id>/delete/',
         views.delete_comment, name='delete-comment'),
]
