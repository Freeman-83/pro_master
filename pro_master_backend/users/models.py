from django.conf import settings
from django.apps import apps
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(UserManager):
    """Кастомный User Manager."""
    
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    username = None
    email = models.EmailField(
        _('email'),
        max_length=254,
        unique=True
    )
    phone_number = PhoneNumberField(
        'Номер телефона',
        unique=True
    )
    is_master = models.BooleanField('Статус Мастера', default=False)

    USERNAME_FIELD = 'email'
    ALT_USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['password']

    objects = CustomUserManager()

    class Meta:
        ordering = ['email']
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'phone_number'],
                name='unique_user'
            ),
        ]

    def __str__(self) -> str:
        return self.email


class ClientProfile(models.Model):
    """Модель профиля Клиента."""
    client = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='clients'
    )
    profile_name = models.CharField(
        'Логин',
        max_length=150,
        null=True,
        blank=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=64,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=64,
        null=True,
        blank=True
    )
    photo = models.ImageField(
        'Фото профиля',
        upload_to='users/image/',
        null=True,
        blank=True
    )
