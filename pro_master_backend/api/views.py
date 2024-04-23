from django.contrib.auth import get_user_model
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from djoser.conf import settings
from djoser.views import UserViewSet

from drf_spectacular.utils import extend_schema, extend_schema_view

from rest_framework import permissions, viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import CategoryFilterSet, ServiceFilterSet

from services.models import (Category,
                             Favorite,
                             Location,
                             Service,
                             Review)

from .permissions import IsAdminOrMasterOrReadOnly, IsAdminOrAuthorOrReadOnly

from .serializers import (CategorySerializer,
                          CommentSerializer,
                          LocationSerializer,
                          MasterContextSerializer,
                          ReviewSerializer,
                          ServiceSerializer,
                          ServiceContextSerializer)

from .utils import create_relation, delete_relation


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Кастомный базовый вьюсет всех пользователей."""

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = [permissions.IsAuthenticated, ]
        return super().get_permissions()


@extend_schema(tags=['Мастера'])
@extend_schema_view(
    list=extend_schema(summary='Получение списка мастеров'),
    create=extend_schema(summary='Создание нового мастера'),
    retrieve=extend_schema(summary='Профиль мастера'),
    update=extend_schema(summary='Изменение профиля мастера'),
    partial_update=extend_schema(summary='Частичное изменение профиля мастера'),
    destroy=extend_schema(summary='Удаление профиля мастера'),
)
class MasterViewSet(CustomUserViewSet):
    """Кастомный вьюсет Мастера."""

    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = settings.PERMISSIONS.master
        return super().get_permissions()

    def get_queryset(self):
        return User.objects.filter(is_master=True)

    def get_serializer_class(self):
        if self.action == "create":
            if settings.USER_CREATE_PASSWORD_RETYPE:
                return settings.SERIALIZERS.user_create_password_retype
            return settings.SERIALIZERS.master_create
        if self.action in ['list', 'retrieve']:
            return settings.SERIALIZERS.master
        return super().get_serializer_class()

    def perform_create(self, serializer, *args, **kwargs):
        return super().perform_create(serializer, is_master=True)
        


@extend_schema(tags=['Клиенты'])
@extend_schema_view(
    list=extend_schema(summary='Получение списка клиентов'),
    create=extend_schema(summary='Создание нового клиента'),
    retrieve=extend_schema(summary='Профиль клиента'),
    update=extend_schema(summary='Изменение профиля клиента'),
    partial_update=extend_schema(summary='Частичное изменение профиля клиента'),
    destroy=extend_schema(summary='Удаление профиля клиента'),
)
class ClientViewSet(CustomUserViewSet):
    """Кастомный вьюсет Клиента."""

    def get_queryset(self):
        if self.action == 'list' and not self.request.user.is_staff:
            return User.objects.filter(is_master=True)
        return User.objects.filter(is_master=False)


@extend_schema(tags=['Сферы деятельности'])
@extend_schema_view(
    list=extend_schema(summary='Список сфер деятельности'),
    retrieve=extend_schema(summary='Сфера деятельности'),
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
    list=extend_schema(summary='Получение списка услуг'),
    create=extend_schema(summary='Создание новой услуги'),
    retrieve=extend_schema(summary='Профиль услуги'),
    update=extend_schema(summary='Изменение профиля услуги'),
    partial_update=extend_schema(summary='Частичное изменение профиля услуги'),
    destroy=extend_schema(summary='Удаление профиля услуги'),
)
class ServiceViewSet(viewsets.ModelViewSet):
    """Вьюсет Сервисов."""
    queryset = Service.objects.select_related(
        'master'
    ).prefetch_related(
        'tags', 'activities', 'locations'
    ).annotate(
        rating=Avg('reviews__score')
    ).all()
    serializer_class = ServiceSerializer
    permission_classes = (IsAdminOrMasterOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ServiceFilterSet

    @extend_schema(summary='Избранное')
    @action(methods=['post', 'delete'],
            detail=True,
            permission_classes=[permissions.IsAuthenticated, ])
    def favorite(self, request, pk):
        if request.method == 'POST':
            return create_relation(request,
                                   Service,
                                   Favorite,
                                   pk,
                                   ServiceContextSerializer,
                                   field='service')
        return delete_relation(request,
                               Service,
                               Favorite,
                               pk,
                               field='service')


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
        service = get_object_or_404(Service, pk=self.kwargs.get('service_id'))
        return service.reviews.select_related('author').all()

    def perform_create(self, serializer):
        service = get_object_or_404(Service, pk=self.kwargs.get('service_id'))
        serializer.save(author=self.request.user, service=service)


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
        service = get_object_or_404(Service, pk=self.kwargs.get('service_id'))
        review = service.reviews.get(pk=self.kwargs.get('review_id'))
        return review.comments.select_related('author').all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            service=self.kwargs.get('service_id')
        )
        serializer.save(author=self.request.user, review=review)

