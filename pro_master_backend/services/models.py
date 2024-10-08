from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as gismodels
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# from colorfield.fields import ColorField

from phonenumber_field.modelfields import PhoneNumberField

from clients.models import ClientProfile


User = get_user_model()


class Category(models.Model):
    """Модель Категории услуги."""

    name = models.CharField(
        'Наименование',
        max_length=256,
        unique=True
    )
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        verbose_name='Родительская категория',
        related_name='child_categories',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Service(models.Model):
    """Модель Услуги."""

    name = models.CharField(
        'Наименование',
        max_length=500
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='Категория',
        related_name='services',
    )
    duration = models.PositiveIntegerField('Длительность выполнения (мин)')
    price = models.IntegerField('Стоимость услуги (руб)')

    class Meta:
        ordering = ['name']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.name


# class Location(gismodels.Model):
#     """Модель Локации."""
#     address = models.CharField(
#         verbose_name='Адрес',
#         max_length=256
#     )
#     point = gismodels.PointField(spatial_index=True)

#     class Meta:
#         ordering = ['address']
#         verbose_name = 'Location'
#         verbose_name_plural = 'Locations'

#     def __str__(self):
#         return self.address


class ServiceProfile(models.Model):
    """Модель Профиля сервиса."""

    name = models.CharField(
        'Имя профиля',
        max_length=256
    )
    categories = models.ManyToManyField(
        Category,
        through='ServiceProfileCategory',
        verbose_name='Категории услуг'
    )
    services = models.ManyToManyField(
        Service,
        through='ServiceProfileService',
        verbose_name='Услуги'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Собственник',
        related_name='service_profiles'
    )
    owner_first_name = models.CharField(
        'Имя',
        max_length=128
    )
    owner_last_name = models.CharField(
        'Фамилия',
        max_length=128
    )
    description = models.TextField('Описание сервиса')
    profile_foto = models.ImageField(
        'Главное фото профиля',
        upload_to='services/profile_foto/',
        null=True,
        blank=True
    )
    phone_number = PhoneNumberField('Контактный номер телефона')
    site_address = models.URLField(
        'Адрес сайта',
        null=True,
        blank=True
    )
    social_network_contacts = models.URLField(
        'Ссылка на аккаунт в социальных сетях',
        max_length=100,
        null=True,
        blank=True
    )
    created = models.DateTimeField(
        'Дата регистрации в приложении',
        auto_now_add=True,
        db_index=True
    )
    is_organization = models.BooleanField(
        'Статус Организации',
        default=False
    )
    # locations = models.ManyToManyField(
    #     Location,
    #     through='LocationService',
    #     verbose_name='Локации'
    # )

    class Meta:
        ordering = ['-created']
        verbose_name = 'Service Profile'
        verbose_name_plural = 'Service Profiles'

    def __str__(self):
        return self.name


class Image(models.Model):
    """Модель Изображения."""

    service_profile = models.ForeignKey(
        ServiceProfile,
        on_delete=models.CASCADE,
        verbose_name='Фото профиля сервиса',
        related_name='profile_images'
    )
    image = models.ImageField(
        'Фото',
        upload_to='services/profile_images'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return self.service_profile.name


class ServiceProfileCategory(models.Model):
    """Модель отношений Профиль сервиса - Категория."""

    service_profile = models.ForeignKey(
        ServiceProfile,
        on_delete=models.CASCADE,
        related_name='in_categories'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='in_service_profiles'
    )

    class Meta:
        verbose_name = 'Sevice Profile - Category'
        verbose_name_plural = 'Sevice Profiles - Categories'
        constraints = [
            models.UniqueConstraint(
                fields=['service_profile', 'category'],
                name='unique_category_for_service_profile'
            )
        ]

    def __str__(self):
        return f'{self.service_profile} - {self.category}'


class ServiceProfileService(models.Model):
    """Модель отношений Профиль сервиса - Услуга."""

    service_profile = models.ForeignKey(
        ServiceProfile,
        on_delete=models.CASCADE,
        related_name='in_services'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='in_service_profiles'
    )

    class Meta:
        verbose_name = 'Sevice Profile - Service'
        verbose_name_plural = 'Sevice Profiles - Services'
        constraints = [
            models.UniqueConstraint(
                fields=['service_profile', 'service'],
                name='unique_service_for_service_profile'
            )
        ]

    def __str__(self):
        return f'{self.service_profile} - {self.service}'


# class LocationService(models.Model):
#     """Модель отношений Локация-Сервис."""
#     location = models.ForeignKey(
#         Location,
#         on_delete=models.CASCADE,
#         related_name='in_services'
#     )
#     service = models.ForeignKey(
#         Service,
#         on_delete=models.CASCADE,
#         related_name='in_locations'
#     )

#     class Meta:
#         ordering = ['location']
#         verbose_name_plural = 'Locations Services'
#         constraints = [
#             models.UniqueConstraint(fields=['location', 'service'],
#                                     name='unique_location_service')
#         ]

#     def __str__(self):
#         return f'{self.location} {self.service}'


class Employee(models.Model):
    """Модель Сотрудника организации."""

    first_name = models.CharField(
        'Имя',
        max_length=64
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=64
    )
    photo = models.ImageField(
        'Фото профиля',
        upload_to='users/image/',
        null=True,
        blank=True
    )
    organization = models.ForeignKey(
        ServiceProfile,
        on_delete=models.CASCADE,
        related_name='employees'
    )
    phone_number = PhoneNumberField(
        'Номер телефона',
        unique=True
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        return self.phone_number


class Review(models.Model):
    """Модель Отзыва."""

    service_profile = models.ForeignKey(
        ServiceProfile,
        verbose_name='Сервис',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField('Текст')
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    author = models.ForeignKey(
        ClientProfile,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['service_profile', 'author'],
                name='unique_review'
            )
        ]


class Comment(models.Model):
    """Модель Комментария к Отзыву."""

    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField('Текст')
    author = models.ForeignKey(
        ClientProfile,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class Favorite(models.Model):
    """Модель избранных Профилей сервисов."""

    client_profile = models.ForeignKey(
        ClientProfile,
        on_delete=models.CASCADE,
        related_name='favorite_services'
    )
    service_profile = models.ForeignKey(
        ServiceProfile,
        on_delete=models.CASCADE,
        related_name='in_favorite_for_clients'
    )

    class Meta:
        ordering = ['service_profile']
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        constraints = [
            models.UniqueConstraint(
                fields=['client_profile', 'service_profile'],
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.client_profile} - {self.service_profile}'
