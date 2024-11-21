from django.urls import path
from .views import SurveySubmitView

urlpatterns = [
    path('submit/', SurveySubmitView.as_view(), name='submit-answer'),
]
