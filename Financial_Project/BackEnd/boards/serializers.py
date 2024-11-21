from rest_framework import serializers
from .models import Post
from django.contrib.auth import get_user_model


class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField(read_only=True)
    liked_by_user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at',
                  'updated_at', 'like_count', 'liked_by_user']
        read_only_fields = ['author']

    def get_like_count(self, obj):
        return obj.like_users.count()

    def get_liked_by_user(self, obj):
        user = self.context['request'].user
        return obj.like_users.filter(pk=user.pk).exists() if user.is_authenticated else False

    # def validate_author(self, value):
    #     User = get_user_model()
    #     try:
    #         user = User.objects.get(pk=value)
    #     except User.DoesNotExist:
    #         raise serializers.ValidationError("Invalid user")
    #     return user

    # # title, content 검증 로직 추가 (필수 여부)
    # def validate_title(self, value):
    #     if not value:
    #         raise serializers.ValidationError("Title is required.")
    #     return value

    # def validate_content(self, value):
    #     if not value:
    #         raise serializers.ValidationError("Content is required.")
    #     return value
