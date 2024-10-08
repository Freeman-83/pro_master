from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from djoser.conf import settings
from djoser.views import UserViewSet

from drf_spectacular.utils import extend_schema, extend_schema_view

from rest_framework import mixins, pagination, permissions, viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from appointments.models import (Appointment,
                                 Schedule)

from clients.models import ClientProfile

from services.models import (Category,
                             Favorite,
                             Image,
                             # Location,
                             Service,
                             ServiceProfile,
                             Review)

from .filters import (CategoryFilterSet,
                      ServiceFilterSet,
                      ServiceProfileFilterSet)

from .permissions import (IsAdminOrMasterOrReadOnly,
                          IsAdminOrAuthorOrReadOnly,
                          IsAdminOrClientOrReadOnly)

from .serializers import (AppointmentSerializer,
                          CategorySerializer,
                          ClientProfileSerializer,
                          CommentSerializer,
                          ImageSerializer,
                        #   LocationSerializer,
                          ServiceSerializer,
                          ServiceProfileContextSerializer,
                          ServiceProfileSerializer,
                          ScheduleSerializer,
                          ReviewSerializer)

from .utils import create_relation, delete_relation


User = get_user_model()


@extend_schema(tags=['Пользователи'])
@extend_schema_view(
    list=extend_schema(summary='Получение списка пользователей'),
    create=extend_schema(summary='Создание пользователя'),
    retrieve=extend_schema(summary='Пользователь'),
    update=extend_schema(summary='Изменение пользователя'),
    partial_update=extend_schema(summary='Частичное изменение пользователя'),
    destroy=extend_schema(summary='Удаление пользователя'),
)
class CustomUserViewSet(UserViewSet):
    """Кастомный базовый вьюсет всех пользователей."""

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = [permissions.IsAuthenticated, ]
        return super().get_permissions()

    def get_queryset(self):
        if self.action == 'list' and not self.request.user.is_staff:
            return User.objects.filter(pk=self.request.user.id)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "create":
            if settings.USER_CREATE_PASSWORD_RETYPE:
                return settings.SERIALIZERS.user_create_password_retype
            return settings.SERIALIZERS.user_create
        if self.action in ['list', 'retrieve']:
            return settings.SERIALIZERS.user
        return super().get_serializer_class()


@extend_schema(tags=['Профили Клиентов'])
@extend_schema_view(
    list=extend_schema(summary='Получение списка клиентов'),
    create=extend_schema(summary='Создание профиля клиента'),
    retrieve=extend_schema(summary='Профиль клиента'),
    update=extend_schema(summary='Изменение профиля клиента'),
    partial_update=extend_schema(summary='Частичное изменение профиля клиента'),
    destroy=extend_schema(summary='Удаление профиля клиента'),
)
class ClientProfileViewSet(viewsets.ModelViewSet):
    """Кастомный вьюсет Клиента."""

    queryset = ClientProfile.objects.all()
    serializer_class = ClientProfileSerializer
    permission_classes = (IsAdminOrClientOrReadOnly,)

    def get_queryset(self):
        if self.action == 'list' and not self.request.user.is_staff:
            return ClientProfile.objects.filter(client=self.request.user)
        return super().get_queryset()

    def perform_create(self, serializer):
        return serializer.save(client=self.request.user)


@extend_schema(tags=['Категории'])
@extend_schema_view(
    list=extend_schema(summary='Список категорий'),
    retrieve=extend_schema(summary='Категория'),
)
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет Категории."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CategoryFilterSet


@extend_schema(tags=['Услуги'])
@extend_schema_view(
    list=extend_schema(summary='Список услуг'),
    retrieve=extend_schema(summary='Услуга'),
)
class ServiceViewSet(viewsets.ModelViewSet):
    """Вьюсет Услуги."""

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ServiceFilterSet
    permission_classes = (permissions.AllowAny,)


@extend_schema(tags=['Профили Сервисов'])
@extend_schema_view(
    list=extend_schema(summary='Получение списка профилей сервисов'),
    create=extend_schema(summary='Создание новго профиля сервиса'),
    retrieve=extend_schema(summary='Профиль сервиса'),
    update=extend_schema(summary='Изменение профиля сервиса'),
    partial_update=extend_schema(summary='Частичное изменение профиля сервиса'),
    destroy=extend_schema(summary='Удаление профиля сервиса'),
)
class ServiceProfileViewSet(viewsets.ModelViewSet):
    """Вьюсет Профиля Сервиса."""

    queryset = ServiceProfile.objects.select_related(
        'owner', 
    ).prefetch_related(
        'categories', 'services'
    ).annotate(
        rating=Avg('reviews__score')
    ).all()
    serializer_class = ServiceProfileSerializer
    permission_classes = (IsAdminOrMasterOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ServiceProfileFilterSet

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    @extend_schema(summary='Избранное')
    @action(methods=['post', 'delete'],
            detail=True,
            permission_classes=[permissions.IsAuthenticated, ])
    def favorite(self, request, pk):
        if request.method == 'POST':
            return create_relation(request,
                                   ServiceProfile,
                                   Favorite,
                                   pk,
                                   ServiceProfileContextSerializer,
                                   field='service_profile')
        return delete_relation(request,
                               ServiceProfile,
                               Favorite,
                               pk,
                               field='service_profile')


@extend_schema(tags=['Изображения'])
@extend_schema_view(
    list=extend_schema(summary='Получение списка изображений профиля сервиса'),
    retrieve=extend_schema(summary='Получение изображения профиля сервиса'),
)
class ImageViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет Отзывов к Сервисам."""

    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (IsAdminOrMasterOrReadOnly,)


@extend_schema(tags=['Отзывы'])
@extend_schema_view(
    list=extend_schema(summary='Получение списка отзывов к услуге'),
    create=extend_schema(summary='Создание нового отзыва к услуге'),
    retrieve=extend_schema(summary='Получение отзыва к услуге'),
    update=extend_schema(summary='Изменение отзыва к услуге'),
    partial_update=extend_schema(summary='Частичное изменение отзыва к услуге'),
    destroy=extend_schema(summary='Удаление отзыва к услуге'),
)
class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет Отзывов к Сервисам."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrAuthorOrReadOnly,)

    def get_queryset(self):
        service_profile = get_object_or_404(
            ServiceProfile,
            pk=self.kwargs.get('profile_id')
        )
        return service_profile.reviews.select_related('author').all()

    def perform_create(self, serializer):
        service_profile = get_object_or_404(
            ServiceProfile,
            pk=self.kwargs.get('profile_id')
        )
        serializer.save(
            author=self.request.user.client_profile,
            service_profile=service_profile
        )


@extend_schema(tags=['Комментарии'])
@extend_schema_view(
    list=extend_schema(summary='Получение списка комментариев к отзыву'),
    create=extend_schema(summary='Создание комментария к отзыву'),
    retrieve=extend_schema(summary='Получение комментария к отзыву'),
    update=extend_schema(summary='Изменение комментария к отзыву'),
    partial_update=extend_schema(summary='Частичное изменение комментария'),
    destroy=extend_schema(summary='Удаление комментария к отзыву'),
)
class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет Комментариев к Отзывам."""

    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrAuthorOrReadOnly,)

    def get_queryset(self):
        service_profile = get_object_or_404(
            ServiceProfile,
            pk=self.kwargs.get('profile_id')
        )
        review = service_profile.reviews.get(pk=self.kwargs.get('review_id'))
        return review.comments.select_related('author').all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            service=self.kwargs.get('profile_id')
        )
        serializer.save(
            author=self.request.user.client_profile,
            review=review
        )


@extend_schema(tags=['Расписания'])
@extend_schema_view(
    list=extend_schema(summary='Получение списка расписаний сервисов'),
    create=extend_schema(summary='Создание расписания сервиса'),
    retrieve=extend_schema(summary='Получение расписания сервиса'),
    update=extend_schema(summary='Изменение расписания сервиса'),
    partial_update=extend_schema(summary='Частичное изменение расписания сервиса'),
    destroy=extend_schema(summary='Удаление расписания сервиса'),
)
class ScheduleViewSet(viewsets.ModelViewSet):
    """Вьюсет Расписания Сервиса."""

    serializer_class = ScheduleSerializer
    permission_classes = (IsAdminOrMasterOrReadOnly,)

    def get_queryset(self):
        service_profile = get_object_or_404(
            ServiceProfile,
            pk=self.kwargs.get('profile_id')
        )
        return service_profile.schedules.all()

    def perform_create(self, serializer):
        service_profile = get_object_or_404(
            ServiceProfile,
            pk=self.kwargs.get('profile_id')
        )
        serializer.save(service_profile=service_profile)


@extend_schema(tags=['Записи'])
@extend_schema_view(
    list=extend_schema(summary='Получение списка записей на услугу'),
    create=extend_schema(summary='Создание записи на услугу'),
    retrieve=extend_schema(summary='Получение записи на услугу'),
    update=extend_schema(summary='Изменение записи на услугу'),
    partial_update=extend_schema(summary='Частичное изменение записи на услугу'),
    destroy=extend_schema(summary='Удаление записи на услугу'),
)
class AppointmentViewSet(viewsets.ModelViewSet):
    """Вьюсет Записи."""

    serializer_class = AppointmentSerializer
    permission_classes = (IsAdminOrClientOrReadOnly,)

    def get_queryset(self):
        service_profile = get_object_or_404(
            ServiceProfile,
            pk=self.kwargs.get('profile_id')
        )
        schedule = service_profile.schedules.get(pk=self.kwargs.get('schedule_id'))
        return schedule.appointments.all()

    def perform_create(self, serializer):
        schedule = get_object_or_404(
            Schedule,
            pk=self.kwargs.get('profile_id'),
            schedule=self.kwargs.get('schedule_id')
        )
        serializer.save(
            schedule=schedule,
            client_profile=self.request.user.client_profile
        )
