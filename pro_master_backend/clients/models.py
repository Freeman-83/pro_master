from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class ClientProfile(models.Model):
    """Модель профиля Клиента."""
    client = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='client_profile'
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

    class Meta:
        ordering = ['client']
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return self.client.email
