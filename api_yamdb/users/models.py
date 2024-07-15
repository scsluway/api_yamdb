from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import regex_validator


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    email = models.EmailField(
        verbose_name='Email',
        max_length=254,
        unique=True,
        blank=False,
    )
    username = models.CharField(
        verbose_name='Username',
        max_length=150,
        unique=True,
        blank=False,
        validators=[regex_validator],
    )
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        blank=True,
        null=True,
        default=Roles.USER,
        verbose_name='Роль',
    )
    bio = models.TextField(verbose_name='Биография', blank=True)
    confirmation_code = models.CharField(
        max_length=5,
        verbose_name='Код подтверждения',
        blank=True,
        editable=False,
    )

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.is_superuser or self.is_staff or self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
