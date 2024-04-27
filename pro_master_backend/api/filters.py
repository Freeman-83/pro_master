from django_filters.rest_framework import (FilterSet,
                                           BooleanFilter,
                                           CharFilter,
                                           ModelMultipleChoiceFilter)

from services.models import (Category,
                             ServiceProfile,)


class CategoryFilterSet(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Category
        fields = ('name',)


class ServiceFilterSet(FilterSet):

    categories = ModelMultipleChoiceFilter(
        field_name='categories__slug',
        to_field_name='slug',
        queryset=Category.objects.all()
    )
    is_favorited = BooleanFilter(
        field_name='in_favorite_for_clients',
        method='is_exist_filter'
    )

    class Meta:
        model = ServiceProfile
        fields = ('categories',)

    def is_exist_filter(self, queryset, name, value):
        lookup = '__'.join([name, 'client'])
        if self.request.user.is_anonymous:
            return queryset
        return queryset.filter(**{lookup: self.request.user})
