# 아래는 vue와 연결할때
# from rest_framework import viewsets
# from .models import Post
# from .serializers import PostSerializer

# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


# 얘는 장고
from django.shortcuts import render, get_object_or_404
from .models import Post

# 게시글 목록을 보여주는 뷰


def post_list(request):
    posts = Post.objects.all()  # 모든 게시글 가져오기
    return render(request, 'boards/post_list.html', {'posts': posts})

# 게시글 디테일을 보여주는 뷰


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'boards/post_detail.html', {'post': post})
