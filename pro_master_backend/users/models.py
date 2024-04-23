from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    username = models.CharField(
        'Логин/Наименование организации',
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        _('email'),
        max_length=254,
        unique=True,
        null=False,
        blank=False
    )
    first_name = models.CharField(
        'Имя',
        max_length=64,
        default='anonimous'
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=64,
        null=True,
        blank=True
    )
    phone_number = PhoneNumberField(
        'Номер телефона',
        unique=True
    )
    photo = models.ImageField(
        'Фото профиля',
        upload_to='users/image/',
        null=True,
        blank=True
    )
    is_master = models.BooleanField('Статус Мастера', default=False)

    USERNAME_FIELD = 'email'
    ALT_USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'password']

    class Meta:
        ordering = ['username']
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email', 'phone_number'],
                name='unique_user'
            ),
        ]

    def __str__(self) -> str:
        return self.username
