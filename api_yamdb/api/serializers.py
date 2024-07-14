from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User
from users.validators import UsernameValidationMixin

from reviews.models import Category, Genre, GenreTitle, Title


class UserSerializer(UsernameValidationMixin, serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserCreateSerializer(
    UsernameValidationMixin, serializers.ModelSerializer
):
    username = serializers.CharField(
        required=True,
        max_length=150,
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        user = User.objects.filter(username=username, email=email).first()
        if not user:
            errors = {}
            if User.objects.filter(username=username).exists():
                errors['username'] = 'User with the same name already exists.'
            if User.objects.filter(email=email).exists():
                errors['email'] = 'User with the same email already exists.'

            if errors:
                raise serializers.ValidationError(errors)
        return data

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        confirmation_code = validated_data.get('confirmation_code')

        user, created = User.objects.update_or_create(
            username=username,
            email=email,
            defaults={'confirmation_code': confirmation_code},
        )

        if created:
            return user
        return validated_data


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Genre


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), many=True, slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            return Title.objects.create(**validated_data)
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            GenreTitle.objects.create(
                genre=genre, title=title)
        return title

    def validate_year(self, value):
        if value > timezone.now().year:
            raise serializers.ValidationError(
                'The year of publication of the work '
                'cannot be greater than the current year.'
            )
        return value


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        rating_data = obj.reviews.values('score')
        return sum(rating_data) // len(rating_data) if rating_data else None
