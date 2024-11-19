
# 아래는 vue와 연동할때
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import SurveyViewSet, QuestionViewSet, SurveyAnswerViewSet

# router = DefaultRouter()
# router.register(r'surveys', SurveyViewSet)
# router.register(r'questions', QuestionViewSet)
# router.register(r'answers', SurveyAnswerViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]


# surveys/urls.py
# from django.urls import path
# surveys/urls.py


# 얘는그냥
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.survey_list, name='survey_list'),  # 설문지 목록
    path('survey/<int:survey_id>/', views.survey_detail,
         name='survey_detail'),  # 설문지 상세
]
