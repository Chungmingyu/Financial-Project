from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404

# views.py
from dj_rest_auth.registration.views import RegisterView
from rest_framework.permissions import AllowAny  # 모든 사용자가 접근 가능하게 설정


class RegisterView(RegisterView):
    permission_classes = [AllowAny]  # 누구나 접근 가능
    throttle_scope = 'dj_rest_auth'
