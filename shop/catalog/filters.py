import django_filters
import catalog.models as m


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = m.Product
        fields = ["price", "freeDelivery", "rating"]
