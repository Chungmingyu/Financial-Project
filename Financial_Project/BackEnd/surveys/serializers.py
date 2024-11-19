# 얘는 나중에 vue에서 쓸때 사용할것 근데 User을 저따구로쓰면 바로에러뜸 나중에 settings로 가져와야댐
# from rest_framework import serializers
# from .models import Survey, Question, SurveyAnswer
# from django.contrib.auth.models import User


# class SurveySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Survey
#         fields = ['id', 'title', 'description',
#                   'user', 'created_at', 'updated_at']


# class QuestionSerializer(serializers.ModelSerializer):
#     survey = serializers.PrimaryKeyRelatedField(
#         queryset=Survey.objects.all())  # 설문지와 연결

#     class Meta:
#         model = Question
#         fields = ['id', 'survey', 'text', 'question_type', 'created_at']


# class SurveyAnswerSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all())  # 사용자와 연결
#     survey = serializers.PrimaryKeyRelatedField(
#         queryset=Survey.objects.all())  # 설문지와 연결
#     question = serializers.PrimaryKeyRelatedField(
#         queryset=Question.objects.all())  # 질문과 연결

#     class Meta:
#         model = SurveyAnswer
#         fields = ['id', 'user', 'survey', 'question', 'answer', 'created_at']
