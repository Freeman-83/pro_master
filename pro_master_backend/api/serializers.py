import re

from geopy import Yandex

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404

from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from djoser.serializers import (UserSerializer,
                                UserCreateSerializer,
                                TokenCreateSerializer)

from services.models import (Category,
                             Comment,
                             Favorite,
                             # Location,
                             # LocationService,
                             ServiceProfile,
                             ServiceProfileCategory,
                             Review)

from users.models import ClientProfile


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
    """Кастомный сериализатор получения токена по email/номеру телефона"""

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
    """Кастомный базовый сериализатор всех пользователей."""

    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'phone_number',
                  'is_master')


class ClientProfileSerializer(serializers.ModelSerializer):
    """Кастомный сериализатор Клиента."""
    client = CustomUserSerializer(read_only=True)
    # favorites_count = serializers.SerializerMethodField()

    class Meta:
        model = ClientProfile
        fields = ('id',
                  'client',
                  'username',
                  'first_name',
                  'last_name',
                #   'favorites_count'
                  )
        
    def validate_username(self, data):
        username = data
        error_symbols_list = []

        for symbol in username:
            if not re.search(r'^[\w.@+-]+\Z', symbol):
                error_symbols_list.append(symbol)
        if error_symbols_list:
            raise serializers.ValidationError(
                f'Символы {"".join(error_symbols_list)} недопустимы'
            )
        return data

    # def get_favorites_count(self, client):
    #     return client.favorite_services.all().count()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор Активностей."""

    class Meta:
        model = Category
        fields = ('id',
                  'name',
                  'description',
                  'slug',
                  'parent',
                  'categories')


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
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )
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
    service = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )
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
        author = request.user
        service = get_object_or_404(
            ServiceProfile,
            pk=self.context['view'].kwargs.get('service_id')
        )
        if author == service.master:
            raise serializers.ValidationError(
                'Запрещено оставлять отзыв о качестве собственных услуг'
            )
        if request.method == 'POST':
            if Review.objects.filter(service=service, author=author):
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
    category = serializers.StringRelatedField(many=True)

    class Meta:
        model = ServiceProfile
        fields = ('id',
                  'name',
                  'category')


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
    # profile_images = Base64ImageField()
    created = serializers.DateTimeField(read_only=True, format='%d.%m.%Y')
    reviews = ReviewContextSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = ServiceProfile
        fields = ('id',
                  'name',
                  'categories',
                  'description',
                  'owner',
                  # 'locations',
                  'profile_foto',
                  # 'profile_images',
                  'phone_number',
                  'site_address',
                  'social_network_contacts',
                  'created',
                  'first_name',
                  'last_name',
                  'reviews',
                  'rating',
                  'is_favorited')

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

    # def validate(self, data):
    #     activities_list = self.initial_data('activities')
    #     tags_list = self.initial_data('tags')

    #     activities = get_validated_field(activities_list, Activity)
    #     tags = get_validated_field(tags_list, Tag)

    #     data.update({'activities': activities,
    #                  'tags': tags})
    #     return data

    @transaction.atomic
    def create(self, validated_data):
        categories_list = validated_data.pop('categories')
        # locations_list = validated_data.pop('locations')
        service_profile = ServiceProfile.objects.create(**validated_data)
        # service.activities.set(activities_list)

        for category in categories_list:
            ServiceProfileCategory.objects.create(
                service_profile=service_profile,
                category=category
            )

        # for location in locations_list:
        #     location = self.get_location(location)
        #     current_location, _ = Location.objects.get_or_create(**location)
        #     LocationService.objects.create(
        #         location=current_location, service=service
        #     )

        return service_profile

    def get_is_favorited(self, service):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.favorite_services.filter(service=service).exists()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['categories'] = instance.categories.values()
        return data
