import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Answer  # Answer 모델 import
from django.contrib.auth import get_user_model


class SurveySubmitView(APIView):
    def post(self, request, *args, **kwargs):
        # 'tendency' 값 받기 (총합 점수)
        tendency = request.data.get('tendency', None)

        if tendency is None:
            return Response({"detail": "No score provided."}, status=status.HTTP_400_BAD_REQUEST)

        # 현재 로그인한 사용자 가져오기
        user = request.user  # 로그인된 유저

        if not user.is_authenticated:
            return Response({"detail": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        # 칭호 목록
        titles = {
            "0-10": [
                "투자 초보",        # 투자의 세계에 막 발을 들인
                "무지의 용사",      # 이정도는 아직 투자에 대해 잘 모르는
                "금융 신입",        # 금융의 세계에서 첫 걸음
            ],
            "11-20": [
                "중급 투자자",       # 어느 정도 투자에 대한 감을 잡은
                "투자 도전자",       # 도전을 멈추지 않는 투자자
                "금융 중수",         # 금융의 중수급 실력자
            ],
            "21-30": [
                "고급 투자자",       # 투자에 대해 깊은 통찰력을 가진
                "숙련된 전략가",     # 치밀한 전략으로 투자를 이끄는
                "금융 마에스트로",   # 금융의 진정한 전문가
            ],
            "31-40": [
                "전설의 투자자",     # 투자계의 전설로 떠오를만한
                "투자의 마스터",     # 누구도 따라올 수 없는 마스터급
                "엘리트 금융 전문가",  # 금융 분야의 엘리트, 전문가의 정수
            ]
        }

        # 점수에 맞는 칭호 선택
        if 0 <= tendency <= 10:
            title = random.choice(titles["0-10"])
        elif 11 <= tendency <= 20:
            title = random.choice(titles["11-20"])
        elif 21 <= tendency <= 30:
            title = random.choice(titles["21-30"])
        elif 31 <= tendency <= 40:
            title = random.choice(titles["31-40"])
        else:
            title = "점수 초과"

        # User 모델의 style 필드에 칭호 할당
        user.style = title
        user.save()

        # Answer 모델에 레코드 저장
        Answer.objects.create(user=user, tendency=tendency)

        # 저장 성공 후 응답
        return Response({
            "detail": f"Survey submitted successfully! Your title: {title}"
        }, status=status.HTTP_200_OK)
