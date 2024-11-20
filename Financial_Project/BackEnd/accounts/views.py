from rest_framework import permissions, generics
from rest_framework import generics, permissions
from .serializers import BoardSerializer
from .models import Board
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
from rest_framework.views import APIView
from .serializers import CustomUserDetailsSerializer, CustomRegisterSerializer
from .serializers import CustomUserUpdateSerializer
from dj_rest_auth.views import LoginView
from django.contrib.auth import authenticate
from .models import DepositProduct, SavingProduct


from dj_rest_auth.registration.views import RegisterView
from rest_framework.permissions import AllowAny  # 모든 사용자가 접근 가능하게 설정


# 회원가입
class RegisterView(RegisterView):
    permission_classes = [AllowAny]  # 누구나 접근 가능
    throttle_scope = 'dj_rest_auth'
    serializer_class = CustomRegisterSerializer

# 로그인 기본 폼


class CustomLoginView(LoginView):
    pass  # 기본 로직을 그대로 사용

# 유저 프로필 뷰


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserDetailsSerializer

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


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = request.user  # 현재 로그인된 유저 객체를 가져옵니다.

        # 기본적으로 개인정보 수정
        if 'nickname' in request.data or 'gender' in request.data or 'age' in request.data:
            serializer = CustomUserUpdateSerializer(
                user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()  # 유저 정보 저장
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 제품 정보 수정 (DepositProduct나 SavingProduct)
        if 'deposit_fin_prdt_cd' in request.data:
            product_data = request.data.get('deposit_fin_prdt_cd')
            try:
                product = DepositProduct.objects.get(id=product_data)
                user.deposit_fin_prdt_cd = product  # 사용자에게 DepositProduct 할당
                user.save()
                return Response({'detail': 'Deposit product updated successfully.'}, status=status.HTTP_200_OK)
            except DepositProduct.DoesNotExist:
                return Response({'detail': 'Deposit product not found.'}, status=status.HTTP_404_NOT_FOUND)

        if 'saving_fin_prdt_cd' in request.data:
            product_data = request.data.get('saving_fin_prdt_cd')
            try:
                product = SavingProduct.objects.get(id=product_data)
                user.saving_fin_prdt_cd = product  # 사용자에게 SavingProduct 할당
                user.save()
                return Response({'detail': 'Saving product updated successfully.'}, status=status.HTTP_200_OK)
            except SavingProduct.DoesNotExist:
                return Response({'detail': 'Saving product not found.'}, status=status.HTTP_404_NOT_FOUND)

        # 요청에 어떤 제품도 없으면
        return Response({'detail': 'No valid data provided to update.'}, status=status.HTTP_400_BAD_REQUEST)

# 게시판 리스트 생성 뷰


class BoardListCreateView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 해당 게시판 디테일 뷰
class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
