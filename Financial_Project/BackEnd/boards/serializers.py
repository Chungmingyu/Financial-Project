# vue랑 연동할때
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content',
                  'author', 'created_at', 'updated_at']

