from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as gismodels
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# from colorfield.fields import ColorField

from phonenumber_field.modelfields import PhoneNumberField


User = get_user_model()


class Category(models.Model):
    """Модель Категории."""
    name = models.CharField('Вид деятельности', unique=True, max_length=256)
    description = models.TextField('Описание', null=False, blank=False)
    slug = models.SlugField('Slug', unique=True, max_length=200)
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name='Родительская категория',
        related_name='categories'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

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


class Service(models.Model):
    """Модель Сервиса."""
    name = models.CharField('Наименование', max_length=256)
    description = models.TextField('Описание', null=False, blank=False)
    master = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Мастер',
        related_name='services'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='services'
    )
    # locations = models.ManyToManyField(
    #     Location,
    #     through='LocationService',
    #     verbose_name='Локации'
    # )
    image = models.ImageField(
        'Фото',
        upload_to='services/image/',
        null=True,
        blank=True
    )
    about_master = models.TextField('О себе', null=True, blank=True)
    site_address = models.URLField(
        'Адрес сайта',
        null=True,
        blank=True
    )
    phone_number = PhoneNumberField('Контактный номер телефона')
    social_network_contacts = models.CharField(
        'Ссылка на аккаунт в социальных сетях',
        max_length=100,
        null=True,
        blank=True
    )
    created = models.DateTimeField(
        'Дата размещения информации', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        default_related_name = 'services'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель Отзыва."""
    service = models.ForeignKey(
        Service,
        verbose_name='Сервис',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField('Текст')
    score = models.PositiveSmallIntegerField(
        'Оценка', validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['service', 'author'],
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
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


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


class Favorite(models.Model):
    """Модель избранных Сервисов."""
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_services'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='in_favorite_for_clients'
    )

    class Meta:
        ordering = ['service']
        constraints = [
            models.UniqueConstraint(fields=['client', 'service'],
                                    name='unique_favorite')
        ]

    def __str__(self):
        return f'{self.client} {self.service}'


class Schedule(models.Model):
    """Модель Расписания услуги."""
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name='Услуга',
        related_name='schedules'
    )
    datetime_start = models.DateTimeField(
        'Начало интервала расписания',
        unique=True
    )
    datetime_end = models.DateTimeField(
        'Конец интервала расписания',
        unique=True
    )

    class Meta:
        ordering = ['datetime_start']
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'
        constraints = [
            models.UniqueConstraint(
                fields=['service', 'datetime_start', 'datetime_end'],
                name='unique_shedule')
        ]

    def __str__(self):
        return f'{self.datetime_start} {self.datetime_end}'


class Appointment(models.Model):
    """Модель Записи на услугу."""
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name='Услуга',
        related_name='appointments'
    )
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Клиент',
        related_name='appointments'
    )
    appointment_datetime_start = models.ForeignKey(
        Schedule,
        to_field='datetime_start',
        on_delete=models.CASCADE,
        verbose_name='Начало интервала записи',
        related_name='appointments_start'
    )
    appointment_datetime_end = models.ForeignKey(
        Schedule,
        to_field='datetime_end',
        on_delete=models.CASCADE,
        verbose_name='Конец интервала записи',
        related_name='appointments_end'
    )

    class Meta:
        ordering = ['appointment_datetime_start']
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        constraints = [
            models.UniqueConstraint(
                fields=['service', 'client', 'appointment_datetime_start'],
                name='unique_appointment')
        ]

    def __str__(self):
        return f'{self.service} {self.client}'
