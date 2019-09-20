

from django_filters import rest_framework as filters

from apps.logistics.models import Region
from apps.user.models import User
from .models import Product, Brand


class ProductFilter(filters.FilterSet):
    """
    商品的过滤类
    """
    # min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    # max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    # Github上，查找django-filter项目，在文档中获得所有Filter的使用说明

    creator = filters.ModelChoiceFilter(queryset=User.objects.all())
    brand = filters.ModelChoiceFilter(queryset=Brand.objects.all())
    # place_delivery = filters.ModelChoiceFilter(queryset=Region.objects.all())

    # 在过滤器中实现模糊搜索 icontains关键字很重要，i表示不区分大小写
    # name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    # brief = filters.CharFilter(field_name='brief', lookup_expr='icontains')
    # desc = filters.CharFilter(field_name='desc', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['creator', 'brief', 'brand', 'desc']
