from .serializers import CustomUserDetailsSerializer
from rest_framework import permissions, generics
from rest_framework import generics, permissions
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from rest_framework import status
from functools import partial
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView, View
from .serializers import CustomUserDetailsSerializer, CustomRegisterSerializer
from .serializers import CustomUserUpdateSerializer
from dj_rest_auth.views import LoginView
from django.contrib.auth import authenticate
from .models import User
from rest_framework.exceptions import NotFound
from moneys.models import UserDeposit

from dj_rest_auth.registration.views import RegisterView
from rest_framework.permissions import AllowAny  # 모든 사용자가 접근 가능하게 설정
from django.http import JsonResponse

from django.shortcuts import get_object_or_404
# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()


class UserDetailByNicknameView(View):
    def get(self, request, nickname):
        user = get_object_or_404(User, nickname=nickname)  # 닉네임으로 사용자 조회
        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "email": user.email,
            "gender": user.gender,
            "age": user.age,
        })


@api_view(['GET', 'PATCH'])
def userdetail(request):
    if request.method == "GET":
        user = request.user
        serializer = CustomUserDetailsSerializer(
            user, context={'request': request})  # UserSerializer 사용
        print(serializer)
        print(user)
        return Response(serializer.data)

    elif request.method == "PATCH":
        user = User.objects.get(pk=request.user.pk)
        data = request.data

        # 수정 가능한 필드만 업데이트
        user.nickname = data.get("nickname", user.nickname)
        user.gender = data.get("gender", user.gender)
        user.age = data.get("age", user.age)

        try:
            user.save()  # 데이터베이스에 저장
            return Response({
                "message": "User details updated successfully.",
                "user_data": {
                    "nickname": user.nickname,
                    "gender": user.gender,
                    "age": user.age,
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# 회원가입


class RegisterView(RegisterView):
    permission_classes = [AllowAny]  # 누구나 접근 가능
    throttle_scope = 'dj_rest_auth'
    serializer_class = CustomRegisterSerializer

# 로그인 기본 폼


class CustomLoginView(LoginView):
    pass  # 기본 로직을 그대로 사용

# 유저 프로필 뷰


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        로그인한 사용자의 정보를 가져오는 API
        """
        serializer = CustomUserDetailsSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        """
        로그인한 사용자의 정보를 수정하는 API
        """
        serializer = CustomUserDetailsSerializer(
            request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 유저 업데이트 뷰
