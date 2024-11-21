from rest_framework import serializers
from .models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'user', 'tendency']  # 필요한 필드 지정
        read_only_fields = ['user']  # user는 자동으로 설정되므로 읽기 전용
