# surveys/views.py

# 아래는 vue에서 보여줄거면 직렬화가 필요해서 일단 넣어뒀습니다

# from rest_framework import viewsets
# from .models import Survey, Question, SurveyAnswer
# from .serializers import SurveySerializer, QuestionSerializer, SurveyAnswerSerializer
# class SurveyViewSet(viewsets.ModelViewSet):
#     queryset = Survey.objects.all()
#     serializer_class = SurveySerializer


# class QuestionViewSet(viewsets.ModelViewSet):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer


# class SurveyAnswerViewSet(viewsets.ModelViewSet):
#     queryset = SurveyAnswer.objects.all()
#     serializer_class = SurveyAnswerSerializer


# 여기는 프론트 안건드리고 장고에서 하려고 임시로 넣어둔것입니다
from django.shortcuts import render, get_object_or_404, redirect
from .models import Survey, Question, SurveyAnswer
from django.contrib.auth import get_user_model


def survey_detail(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    questions = survey.questions.all()

    if request.method == 'POST':
        # POST 요청 시, 답변을 저장
        for question in questions:
            answer = request.POST.get(f'answer_{question.id}')
            if answer:
                SurveyAnswer.objects.create(
                    user=request.user,  # 현재 로그인한 사용자
                    survey=survey,
                    question=question,
                    answer=answer
                )
        return redirect('survey_list')  # 답변을 저장한 후 설문지 목록 페이지로 리디렉션

    return render(request, 'surveys/survey_detail.html', {'survey': survey, 'questions': questions})
