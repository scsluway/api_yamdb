from rest_framework import serializers

from .models import (Comment, MINIMUM_RATING_VALUE,
                     MAXIMUM_RATING_VALUE, Review)


class ReviewSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True)
    score = serializers.IntegerField(
        required=True,
        min_value=MINIMUM_RATING_VALUE,
        max_value=MAXIMUM_RATING_VALUE)

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'pub_date', 'text', 'author', 'review')
        read_only_fields = ('review',)
