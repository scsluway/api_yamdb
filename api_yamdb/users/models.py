from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import regex_validator


class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    email = models.EmailField(
        verbose_name='Email',
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
    ROLES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )
    role = models.CharField(
        max_length=max(len(label) for _, label in ROLES),
        choices=ROLES,
        blank=True,
        null=True,
        default='user',
        verbose_name='Роль'
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    confirmation_code = models.CharField(
        max_length=5,
        verbose_name='Код подтверждения',
        blank=True
    )

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.is_superuser or self.is_staff or self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'