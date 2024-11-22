# 아래는 vue와 연결할때
from rest_framework import viewsets
# from yaml import serialize
from .models import Post
from .serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# 얘는 장고
from django.shortcuts import render, get_object_or_404
from .models import Post

# 게시글 댓글
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Post, Comment
import json

User = get_user_model()


@require_http_methods(["DELETE"])
@csrf_exempt
def delete_comment(request, comment_id):
    try:
        # DELETE 요청의 본문에서 JSON 데이터를 읽기
        body = json.loads(request.body)
        user_pk = body.get('user_pk')

        # user_pk가 제공되지 않았거나 잘못된 경우
        if not user_pk:
            return JsonResponse({"message": "사용자 정보가 제공되지 않았습니다."}, status=400)

        # 사용자 확인
        user = get_object_or_404(User, pk=user_pk)

        # 댓글 확인
        comment = get_object_or_404(Comment, id=comment_id)

        # 댓글 작성자인지 확인
        if user == comment.author:
            comment.delete()
            return JsonResponse({"message": "댓글이 성공적으로 삭제되었습니다."}, status=200)
        else:
            return JsonResponse({"message": "본인이 쓴 댓글만 지울 수 있습니다."}, status=403)

    except json.JSONDecodeError:
        return JsonResponse({"message": "잘못된 데이터 형식입니다."}, status=400)

    except User.DoesNotExist:
        return JsonResponse({"message": "사용자를 찾을 수 없습니다."}, status=404)

    except Comment.DoesNotExist:
        return JsonResponse({"message": "댓글을 찾을 수 없습니다."}, status=404)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def comment_view(request, post_id):
    # 게시물 확인
    post = get_object_or_404(Post, id=post_id)

    if request.method == "GET":
        comments = post.comments.all()
        comments_data = [
            {
                "id": comment.id,
                "author": comment.author.username,
                "content": comment.content,
                "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for comment in comments
        ]
        return JsonResponse({"comments": comments_data}, status=200)

    elif request.method == "POST":
        # 현재 로그인된 사용자 확인
        user = User.objects.get(pk=request.POST.get('user_pk'))
        if user.is_anonymous:
            return JsonResponse({"error": "로그인이 필요합니다."}, status=401)

        # POST 데이터에서 content 읽기
        content = request.POST.get('content') or request.body.decode('utf-8')

        if not content:
            return JsonResponse({"error": "댓글 내용을 입력해주세요."}, status=400)

        # 댓글 생성
        comment = Comment.objects.create(
            post=post, author=user, content=content
        )
        return JsonResponse({
            "message": "댓글 생성이 완료되었습니다.",
            "comment": {
                "id": comment.id,
                "post_id": post.id,
                "content": comment.content,
                "author": comment.author.username,
            }
        }, status=201)

    return JsonResponse({"error": "Invalid method."}, status=405)


# 게시글 보여주기
class PostListAPIView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request):
        posts = Post.objects.all().order_by("-created_at")
        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

# 게시글 생성


class PostCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # serializer의 data를 request.data로 전달, context는 request를 추가
            serializer = PostSerializer(
                data=request.data, context={'request': request})
            # serializer['nickname'] = request.user.nickname
            if serializer.is_valid(raise_exception=True):
                # User 객체를 찾고, 그것을 save()에 전달
                serializer.save(author=request.user)
                response_data = serializer.data
                response_data['nickname'] = request.user.nickname
                return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Exception occurred: {str(e)}")  # 예외 발생 시 출력
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 게시글 디테일을 보여주는 뷰
@require_http_methods(["GET"])
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    serializer = PostSerializer(post, context={'request': request})
    return JsonResponse(serializer.data, safe=False)
    # return Response(serializer.data)

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
