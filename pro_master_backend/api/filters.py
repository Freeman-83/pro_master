from django_filters.rest_framework import (BooleanFilter,
                                           CharFilter,
                                           FilterSet,
                                           ModelMultipleChoiceFilter)

from services.models import (Category,
                             Service,
                             ServiceProfile)


class CategoryFilterSet(FilterSet):
    """Фильтр Категорий."""

    name = CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Category
        fields = ('name',)


class ServiceFilterSet(FilterSet):
    """Фильтр Услуг."""

    name = CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Service
        fields = ('name',)


class ServiceProfileFilterSet(FilterSet):
    """Фильтр Профилей сервисов по категориям, услугам, наличию в избранном."""

    categories = ModelMultipleChoiceFilter(
        field_name='categories__name',
        to_field_name='name',
        queryset=Category.objects.all()
    )
    services = ModelMultipleChoiceFilter(
        field_name='services__name',
        to_field_name='name',
        queryset=Service.objects.all()
    )
    is_favorited = BooleanFilter(
        field_name='in_favorite_for_clients',
        method='is_exist_filter'
    )

    class Meta:
        model = ServiceProfile
        fields = ('categories',)

    def is_exist_filter(self, queryset, name, value):
        lookup = '__'.join([name, 'client_profile'])
        if self.request.user.is_anonymous:
            return queryset
        return queryset.filter(**{lookup: self.request.user.client_profile})
