# 아래는 vue와 연결할때
from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.conf import settings
from django.contrib.auth import get_user_model

# 얘는 장고
from django.shortcuts import render, get_object_or_404
from .models import Post


# 게시글 보여주기
class PostListAPIView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request):
        posts = Post.objects.all().order_by("-created_at")
        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

# 게시글 생성


User = get_user_model()


class PostCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # serializer의 data를 request.data로 전달, context는 request를 추가
            serializer = PostSerializer(
                data=request.data, context={'request': request})

            if serializer.is_valid(raise_exception=True):
                # User 객체를 찾고, 그것을 save()에 전달
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Exception occurred: {str(e)}")  # 예외 발생 시 출력
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 게시글 디테일을 보여주는 뷰

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'boards/post_detail.html', {'post': post})

# 좋아요 기능


class ToggleLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if post.like_users.filter(pk=request.user.pk).exists():
            post.like_users.remove(request.user)

        else:
            post.like_users.add(request.user)
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)
#         like, created = Like.objects.get_or_create(
#             user=request.user, post=post)

#         if not created:  # 이미 좋아요를 눌렀으면 삭제
#             like.delete()
#             liked = False
#         else:  # 새로 좋아요 추가
#             liked = True

#         return Response({
#             'liked': liked,
#             'like_count': post.likes.count()
    # })

# 게시글 삭제


class PostDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(
                id=post_id, author=request.user)  # 본인이 작성한 글만 삭제 가능
            post.delete()
            return Response({"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({"error": "Post not found or not authorized"}, status=status.HTTP_404_NOT_FOUND)
