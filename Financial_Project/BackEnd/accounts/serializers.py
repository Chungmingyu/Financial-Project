from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
UserModel = get_user_model()


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
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'nickname': self.validated_data.get('nickname', ''),
            'gender': self.validated_data.get('gender', ''),
            'age': self.validated_data.get('age', -1),  # 기본값 -1을 사용
            'email': self.validated_data.get('email', '')  # 이메일 추가
        }

    def save(self, request):
        # 부모 클래스의 save 메서드를 호출하여 사용자 생성
        user = super().save(request)

        # 유효성 검사된 데이터를 사용하여 추가 필드들 저장
        user.nickname = self.validated_data.get('nickname', '')
        user.gender = self.validated_data.get('gender', '')
        user.age = self.validated_data.get('age', -1)  # 기본값을 -1로 설정
        user.email = self.validated_data.get('email', '')  # 이메일 저장

        # 변경된 사용자 정보 저장
        user.save()

        return user


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        extra_fields = []
        # see https://github.com/iMerica/dj-rest-auth/issues/181
        # UserModel.XYZ causing attribute error while importing other
        # classes from `serializers.py`. So, we need to check whether the auth model has
        # the attribute or not
        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'first_name'):
            extra_fields.append('first_name')
        if hasattr(UserModel, 'last_name'):
            extra_fields.append('last_name')
        if hasattr(UserModel, 'nickname'):
            extra_fields.append('nickname')
        if hasattr(UserModel, 'age'):
            extra_fields.append('age')
        if hasattr(UserModel, 'email'):
            extra_fields.append('email')
        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)


class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'gender', 'age']  # 수정할 필드들만 포함

    def update(self, instance, validated_data):
        # 인스턴스에서 각 필드를 업데이트합니다.
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.age = validated_data.get('age', instance.age)
        instance.save()
        return instance
