# 아래는 vue와 연결할때
from rest_framework import viewsets
# from yaml import serialize
from .models import Post
from .serializers import PostSerializer, CommentSerializers
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
from rest_framework.decorators import api_view, permission_classes

User = get_user_model()


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request):
    # 클라이언트에서 postId를 요청 본문에 전달한다고 가정
    post_id = request.data.get('postId')

    if not post_id:
        return Response({'error': 'postId is required'}, status=400)

    # Post 객체 가져오기
    post = get_object_or_404(Post, pk=post_id)

    # 권한 체크: 작성자인지 확인
    if post.author != request.user:
        return Response({'error': 'You do not have permission to delete this post.'}, status=403)

    # 게시글 삭제
    post.delete()
    return Response({'message': 'Post deleted successfully.'}, status=200)


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
        comments = post.comments.all().order_by('-created_at')  # 내림차순 정렬 추가
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
        # 사용자 확인
        user_pk = request.POST.get('user_pk')
        if not user_pk:
            return JsonResponse({"error": "유효하지 않은 사용자입니다."}, status=400)
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return JsonResponse({"error": "사용자를 찾을 수 없습니다."}, status=404)

        if user.is_anonymous:
            return JsonResponse({"error": "로그인이 필요합니다."}, status=401)

        # POST 데이터에서 content 읽기
        content = request.POST.get('content')

        if not content:
            return JsonResponse({"error": "댓글 내용을 입력해주세요."}, status=400)

        # 댓글 생성
        comment = Comment.objects.create(
            post=post, author=user, content=content
        )
        return JsonResponse(
            {
                "comment": {
                    "id": comment.id,
                    "author": comment.author.nickname,  # 닉네임 사용
                    "content": comment.content,
                    "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
            },
            status=201,
        )

    return JsonResponse({"error": "Invalid method."}, status=405)


# 게시글 보여주기
class PostListAPIView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request):
        posts = Post.objects.all().order_by("-created_at")
        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        print(serializer.data)
        return Response(serializer.data)

# 게시글 생성


class PostCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # serializer의 data를 request.data로 전달, context는 request를 추가
            serializer = PostSerializer(
                data=request.data, context={'request': request})
            print(serializer, '@@@@@@')
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
