from django.contrib.auth import authenticate, login
from django.http import JsonResponse
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
from rest_framework.views import APIView
from yaml import serialize
from .serializers import CustomUserDetailsSerializer
from .serializers import CustomUserUpdateSerializer
from dj_rest_auth.views import LoginView
from django.contrib.auth import authenticate

# views.py
from dj_rest_auth.registration.views import RegisterView
from rest_framework.permissions import AllowAny  # 모든 사용자가 접근 가능하게 설정


class RegisterView(RegisterView):
    permission_classes = [AllowAny]  # 누구나 접근 가능
    throttle_scope = 'dj_rest_auth'


# views.py


class CustomLoginView(LoginView):
    pass  # 기본 로직을 그대로 사용


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
        # 사용자 정보를 수정하는 경우
        serializer = CustomUserDetailsSerializer(
            request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = request.user  # 현재 로그인된 유저 객체를 가져옵니다.
        serializer = CustomUserUpdateSerializer(
            user, data=request.data, partial=True)  # 일부 필드만 업데이트

        if serializer.is_valid():
            serializer.save()  # 유저 정보 저장
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
