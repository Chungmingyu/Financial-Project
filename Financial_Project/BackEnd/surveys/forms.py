# django에서 연동할때 필요함 vue할땐 지워도됨
from django.shortcuts import render, get_object_or_404, redirect
from .models import Survey, Question, SurveyAnswer
from django.contrib.auth.models import User


def survey_detail(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    questions = survey.questions.all()

    if request.method == 'POST':
        # POST 요청 시, 답변을 저장
        for question in questions:
            answer = request.POST.get(f'answer_{question.id}')
            if answer:
                SurveyAnswer.objects.create(
                    user=request.user,
                    survey=survey,
                    question=question,
                    answer=answer
                )
        return redirect('survey_list')  # 답변을 저장한 후 설문지 목록 페이지로 리디렉션

    return render(request, 'surveys/survey_detail.html', {'survey': survey, 'questions': questions})
