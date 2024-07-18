from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

LIMITED_TITLE_OUTPUT = 20
MINIMUM_RATING_VALUE = 1
MAXIMUM_RATING_VALUE = 10
MAX_NAME_LENGTH = 256
MAX_SLUG_FIELD = 50
MAX_TEXT_LENGTH = 500

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH, verbose_name='Имя')
    slug = models.SlugField(
        unique=True,
        max_length=MAX_SLUG_FIELD,
        verbose_name='Слаг'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:LIMITED_TITLE_OUTPUT]


class Genre(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH, verbose_name='Имя')
    slug = models.SlugField(
        unique=True,
        max_length=MAX_SLUG_FIELD,
        verbose_name='Слаг'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:LIMITED_TITLE_OUTPUT]


class Title(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH, verbose_name='Имя')
    year = models.PositiveSmallIntegerField(db_index=True, verbose_name='Год')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        verbose_name='Категории'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        through='GenreTitle',
        verbose_name='жанры'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:LIMITED_TITLE_OUTPUT]


class Review(models.Model):
    text = models.CharField(max_length=MAX_TEXT_LENGTH, verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        default=1, verbose_name='Автор'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(MINIMUM_RATING_VALUE),
            MaxValueValidator(MAXIMUM_RATING_VALUE)
        ],
        verbose_name='Рейтинг'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_review'
            )
        ]

    def __str__(self):
        return self.text[:LIMITED_TITLE_OUTPUT]


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:LIMITED_TITLE_OUTPUT]


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre_titles',
        null=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genre_titles',
        null=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['genre', 'title'], name='unique_genre_title'
            )
        ]
