from django.contrib.auth import get_user_model
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from djoser.conf import settings
from djoser.views import UserViewSet

from drf_spectacular.utils import extend_schema, extend_schema_view

from rest_framework import mixins, permissions, viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import CategoryFilterSet, ServiceProfileFilterSet

from services.models import (Category,
                             Favorite,
                             # Location,
                             ServiceProfile,
                             Review)

from users.models import ClientProfile


from .permissions import (IsAdminOrMasterOrReadOnly,
                          IsAdminOrAuthorOrReadOnly,
                          IsAdminOrClientOrReadOnly)

from .serializers import (CategorySerializer,
                          ClientProfileSerializer,
                          CommentSerializer,
                        #   LocationSerializer,
                          ServiceProfileContextSerializer,
                          ServiceProfileSerializer,
                          ReviewSerializer)

from .utils import create_relation, delete_relation


User = get_user_model()


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
            return ClientProfile.objects.filter(pk=self.request.user.id)
        return super().get_queryset()

    def perform_create(self, serializer):
        return serializer.save(client=self.request.user)


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
        'categories'
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
                                   field='profile')
        return delete_relation(request,
                               ServiceProfile,
                               Favorite,
                               pk,
                               field='profile')


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
        service = get_object_or_404(
            ServiceProfile,
            pk=self.kwargs.get('profile_id')
        )
        return service.reviews.select_related('author').all()

    def perform_create(self, serializer):
        service = get_object_or_404(
            ServiceProfile,
            pk=self.kwargs.get('profile_id')
        )
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
        service = get_object_or_404(
            ServiceProfile,
            pk=self.kwargs.get('profile_id')
        )
        review = service.reviews.get(pk=self.kwargs.get('review_id'))
        return review.comments.select_related('author').all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            service=self.kwargs.get('service_id')
        )
        serializer.save(author=self.request.user, review=review)

