from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response

from .models import Comment, Review, Title
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True)
    score = serializers.IntegerField(required=True)
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author',)

    def validate(self, attrs):
        if 0 > attrs['score'] or attrs['score'] > 10:
            raise serializers.ValidationError(
                'Оценка от 0 до 10'
            )

        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'pub_date', 'text', 'author', 'review')
        read_only_fields = ('review',)
