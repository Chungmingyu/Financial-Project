# surveys/models.py
from django.conf import settings
from django.db import models

# 설문지모델


class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    tendency = models.IntegerField()
    

# class Survey(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField(null=True, blank=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                              on_delete=models.CASCADE)  # 확장된 User 모델을 참조
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title


# # 질문지모델
# class Question(models.Model):
#     survey = models.ForeignKey(
#         Survey, on_delete=models.CASCADE, related_name="questions")
#     text = models.CharField(max_length=255)
#     question_type = models.CharField(max_length=50, choices=[(
#         'text', 'Text'), ('multiple', 'Multiple Choice')])
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.text


# # 답변 저장할 모델
# class SurveyAnswer(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                              on_delete=models.CASCADE)  # 확장된 User 모델을 참조
#     survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     answer = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Answer by {self.user} to {self.question.text}"
