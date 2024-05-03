import re

from geopy import Yandex

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404

from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from djoser.serializers import (UserSerializer,
                                UserCreateSerializer,
                                TokenCreateSerializer)

from services.models import (Appointment,
                             Category,
                             Comment,
                             Employee,
                             Favorite,
                             Image,
                             # Location,
                             # LocationService,
                             ServiceProfile,
                             ServiceType,
                             ServiceProfileCategory,
                             Schedule,
                             Review)

from users.models import ClientProfile

from .utils import get_validated_field


User = get_user_model()


class RegisterUserSerializer(UserCreateSerializer):
    """Кастомный базовый сериализатор регистрации пользователя."""

    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'phone_number',
                  'password',
                  'is_master')


class CustomTokenCreateSerializer(TokenCreateSerializer):
    """Кастомный сериализатор получения токена по email/номеру телефона."""

    password = serializers.CharField(
        required=False, style={'input_type': 'password'}
    )
    field = User.USERNAME_FIELD
    alt_field = User.ALT_USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

        if self.context['request'].data.get(self.field):
            self.fields[self.field] = serializers.CharField(required=False)
        else:
            self.fields[self.alt_field] = serializers.CharField(required=False)

    def validate(self, data):
        password = data.get('password')

        params = {}
        if self.context['request'].data.get(self.field):
            params = {self.field: data.get(self.field)}
        else:
            params = {self.alt_field: data.get(self.alt_field)}
        self.user = authenticate(
            request=self.context.get('request'), **params, password=password
        )

        if not self.user:
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                raise serializers.ValidationError(
                    'Некорректный пароль пользователя!'
                )
        if self.user and self.user.is_active:
            return data
        raise serializers.ValidationError(
            'Некорректные данные пользователя!'
        )


class CustomUserSerializer(UserSerializer):
    """Кастомный базовый сериализатор всех типов пользователей."""

    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'phone_number',
                  'is_master')


class ClientProfileSerializer(serializers.ModelSerializer):
    """Кастомный сериализатор Клиента."""
    client = CustomUserSerializer(
        default=serializers.CurrentUserDefault()
    )
    favorites_count = serializers.SerializerMethodField()

    class Meta:
        model = ClientProfile
        fields = ('id',
                  'client',
                  'profile_name',
                  'first_name',
                  'last_name',
                  'favorites_count')

    @transaction.atomic
    def create(self, validated_data):
        return super().create(validated_data)

    def get_favorites_count(self, profile):
        return profile.client.favorite_services.all().count()


class ServiceTypeSerializer(serializers.ModelSerializer):
    """Сериализатор Типа Сервиса."""

    class Meta:
        model = ServiceType
        fields = ('id',
                  'name')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор Категории."""

    class Meta:
        model = Category
        fields = ('id',
                  'name',
                  'parent_category')


# class LocationSerializer(serializers.ModelSerializer):
#     """Сериализатор Локации."""
#     address = serializers.CharField(required=False)
#     point = serializers.CharField(required=False)

#     class Meta:
#         model = Location
#         fields = ('id',
#                   'address',
#                   'point')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор Комментариев к Отзывам."""
    author = ClientProfileSerializer(read_only=True)
    pub_date = serializers.DateTimeField(read_only=True, format='%d.%m.%Y')

    class Meta:
        model = Comment
        fields = ('id',
                  'review',
                  'text',
                  'author',
                  'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор Отзывов к Сервисам."""
    service_profile = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = ClientProfileSerializer(read_only=True)
    pub_date = serializers.DateTimeField(read_only=True, format='%d.%m.%Y')
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Review
        fields = ('id',
                  'service',
                  'author',
                  'text',
                  'score',
                  'pub_date',
                  'comments')

    def validate(self, data):
        request = self.context['request']
        author = request.user.client_profile
        service_profile = get_object_or_404(
            ServiceProfile,
            pk=self.context['view'].kwargs.get('profile_id')
        )
        if author == service_profile.owner:
            raise serializers.ValidationError(
                'Запрещено оставлять отзыв о качестве собственных услуг'
            )
        if request.method == 'POST':
            if Review.objects.filter(
                service_profile=service_profile, author=author
            ):
                raise serializers.ValidationError(
                    'Можно оставить только один отзыв'
                )
        return data


class ReviewContextSerializer(serializers.ModelSerializer):
    """Сериализатор Отзывов к Сервисам в других контекстах."""
    pub_date = serializers.DateTimeField(read_only=True, format='%d.%m.%Y')

    class Meta:
        model = Review
        fields = ('id', 'text', 'score', 'author', 'pub_date')


class ServiceProfileContextSerializer(serializers.ModelSerializer):
    """Сериализатор отображения профиля рецепта в других контекстах."""
    service_type = ServiceTypeSerializer(read_only=True)
    category = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = ServiceProfile
        fields = ('id',
                  'name',
                  'service_type',
                  'category')


class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор изображений профиля сервиса."""

    class Meta:
        model = Image
        fields = ('id',
                  'service_profile',
                  'image')
        

class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор Сотрудника организации."""
    organization = ServiceProfileContextSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = ('id',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'organization')


class ServiceProfileSerializer(serializers.ModelSerializer):
    """Сериализатор профиля Сервиса."""
    owner = CustomUserSerializer(
        default=serializers.CurrentUserDefault()
    )
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True
    )
    # locations = LocationSerializer(many=True)
    profile_foto = Base64ImageField()
    profile_images = ImageSerializer(read_only=True, many=True)
    uploaded_images = serializers.ListField(
        child=Base64ImageField(), write_only=True
    )
    created = serializers.DateTimeField(read_only=True, format='%d.%m.%Y')
    employees = EmployeeSerializer(read_only=True, many=True)
    employees_count = serializers.SerializerMethodField()
    reviews = ReviewContextSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = ServiceProfile
        fields = ('id',
                  'name',
                  'service_type',
                  'categories',
                  'owner',
                  'description',
                  'first_name',
                  'last_name',
                  # 'locations',
                  'profile_foto',
                  'profile_images',
                  'uploaded_images',
                  'phone_number',
                  'site_address',
                  'social_network_contacts',
                  'created',
                  'employees',
                  'employees_count',
                  'reviews',
                  'rating',
                  'is_favorited')
        depth = 5

        validators = [
            UniqueTogetherValidator(queryset=ServiceProfile.objects.all(),
                                    fields=['owner', 'name'])
        ]

    # def get_location(self, location):
    #     if location.get('address'):
    #         location_data = Yandex(
    #             api_key=settings.API_KEY
    #         ).geocode(location['address'])
    #         location['address'] = location_data.address
    #         location['point'] = f'POINT({location_data.longitude} {location_data.latitude})'

    #     elif location.get('point'):
    #         point = location.get('point')
    #         location_data = Yandex(api_key=settings.API_KEY).reverse(point)

    #         location['address'] = location_data.address
    #         location['point'] = f'POINT({point})'

    #     return location

    @transaction.atomic
    def create(self, validated_data):
        categories_list = validated_data.pop('categories')
        images = validated_data.pop('uploaded_images')
        # locations_list = validated_data.pop('locations')

        service_profile = ServiceProfile.objects.create(**validated_data)

        service_profile.categories.set(categories_list)

        for image in images:
            Image.objects.create(service_profile=service_profile, image=image)

        # for location in locations_list:
        #     location = self.get_location(location)
        #     current_location, _ = Location.objects.get_or_create(**location)
        #     LocationService.objects.create(
        #         location=current_location, service=service
        #     )

        return service_profile
    
    @transaction.atomic
    def update(self, instance, validated_data):
        categories_list = validated_data.pop('categories', instance.categories)

        images_objects = Image.objects.filter(service_profile=instance)
        images_list = [obj.image for obj in images_objects]
        images_list = validated_data.pop('uploaded_images', images_list)
        
        # locations_list = validated_data.pop('locations')

        instance = super().update(instance, validated_data)
        instance.save()

        instance.categories.clear()
        instance.categories.set(categories_list)

        for image in images_list:
            Image.objects.update_or_create(
                service_profile=instance, image=image
            )

        # instance.locations.clear()
        # instance.locations.set(locations_list)

        return instance
    
    def get_employees_count(self, service):
        return 1 + service.employees.count()

    def get_is_favorited(self, service_profile):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.favorite_services.filter(
            service_profile=service_profile
        ).exists()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['categories'] = instance.categories.values()
        data['service_type'] = instance.service_type.name
        return data


class ScheduleSerializer(serializers.ModelSerializer):
    """Сериализатор Расписания работы Сервиса."""
    service_profile = ServiceProfileContextSerializer(read_only=True)

    class Meta:
        model = Schedule
        fields = ('id',
                  'service_profile',
                  'date',
                  'start',
                  'end')


class AppointmentSerializer(serializers.ModelSerializer):
    """Сериализатор Расписания работы Сервиса."""
    # service_profile = ServiceProfileContextSerializer(read_only=True)
    client_profile = ClientProfileSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ('id',
                  'schedule',
                  'client_profile',
                  'appointment_time')
