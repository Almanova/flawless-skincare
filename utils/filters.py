import django_filters

from core.models import Product


class ProductFilter(django_filters.FilterSet):
    max_price = django_filters.NumberFilter(field_name='price',
                                            lookup_expr='lte')
    min_price = django_filters.NumberFilter(field_name='price',
                                            lookup_expr='gte')
    max_rating = django_filters.NumberFilter(field_name='rating',
                                             lookup_expr='lte')
    min_rating = django_filters.NumberFilter(field_name='rating',
                                             lookup_expr='gte')

    class Meta:
        model = Product
        fields = ('category', 'price', 'discount', 'rating', 'brand')
