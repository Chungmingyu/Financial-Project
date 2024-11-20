"""
URL configuration for moneystark project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('moneys/', include('moneys.urls')),
    path('exchanges/', include('exchanges.urls')),
    path('accounts/', include('dj_rest_auth.urls')),  # 기본 인증 URL
    path('accounts/signup/', include('dj_rest_auth.registration.urls')),  # 회원가입 관련 URL
    path('accounts/logout/', include('dj_rest_auth.urls')),  # 로그아웃 관련 URL
    path('accounts/user/', include('dj_rest_auth.urls')),  # 사용자 정보 조회 및 업데이트
    path('bankmap/', include('bankmap.urls')),
    path('surveys/', include('surveys.urls')),  # 설문지 관련 URL
    path('boards/', include('boards.urls')),  # boards 앱 연결
]
