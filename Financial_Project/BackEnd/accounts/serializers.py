from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers


class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(
        required=True,
        max_length=10
    )
    gender = serializers.ChoiceField(
        choices=(('M', '남성(Man)'), ('W', '여성(Woman)')),
        required=True
    )
    age = serializers.IntegerField(
        required=True,
        min_value=0
    )
    email = serializers.EmailField(
        required=True,
        allow_blank=False
    )

    def get_cleaned_data(self):
        # 기본 필드와 커스텀 필드 포함
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname', '')
        data['gender'] = self.validated_data.get('gender', '')
        data['age'] = self.validated_data.get('age', '')
        return data

    def save(self, request):
        # 부모 클래스의 save 메서드를 호출하여 사용자 생성
        user = super().save(request)
        user.nickname = self.validated_data.get('nickname', '')
        user.gender = self.validated_data.get('gender', '')
        user.age = self.validated_data.get('age', '')
        user.save()
        return user
