from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

LIMIT_ON_NUMBER_OF_LETTERS = 20

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Имя')
    slug = models.SlugField(unique=True, max_length=50, verbose_name='Слаг')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:LIMIT_ON_NUMBER_OF_LETTERS]


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Имя')
    slug = models.SlugField(unique=True, max_length=50, verbose_name='Слаг')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:LIMIT_ON_NUMBER_OF_LETTERS]


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='Имя')
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
        return self.name[:LIMIT_ON_NUMBER_OF_LETTERS]


class Review(models.Model):
    text = models.CharField(max_length=500)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        default=1,  # Здесь используется ID пользователя по умолчанию
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_review'
            )
        ]

    def __str__(self):
        return self.text[:LIMIT_ON_NUMBER_OF_LETTERS]


class Comment(models.Model):
    text = models.TextField()
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)


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
