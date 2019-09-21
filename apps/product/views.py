import time

import os

from django.http import HttpResponse

import xlrd
from rest_framework import viewsets, mixins, filters
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from django_filters.rest_framework import DjangoFilterBackend

from apps.product.filters import ProductFilter
from apps.product.models import Category, Product
from apps.product.utils import import_multi_products

from bigmarket.paginations import CommenPagination

from .serializers import ProductSerializer, CategorySerializer


class InitialCategoryView(APIView):
    """
    初始化地区数据
    从.xls导入
    1列:id  2列:pid  3列:name  4列:level  5列:spell  6列:sort
    """
    def get(self, request):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        print(ROOT_DIR)
        file = ROOT_DIR + '\\initial_data\\t_category.xls'
        print(file)
        # """
        wb = xlrd.open_workbook(filename=file)  # 打开文件
        table = wb.sheet_by_index(0)  # 取第一张工作簿
        rows_count = table.nrows  # 取总行数

        for row_index in range(rows_count):  # 行循环

            category = Category()
            row_data = table.row_values(row_index)

            category.id = int(row_data[0])
            if Category.objects.filter(id__exact=int(row_data[0])):
                continue
            category.name = row_data[1]
            category.level = int(row_data[2])
            if row_data[3] is not None and row_data[3] != '' and row_data[3] != 0:
                query_set = Category.objects.filter(id__exact=int(row_data[3]))
                if query_set:
                    category.parent = query_set[0]
                else:
                    category.parent = None
            else:
                category.parent = None

            temp_str = str(category.id) + ' - ' + str(category.name) + ' - '
            if category.parent:
                temp_str += category.parent.name
            else:
                temp_str += 'None'
            print(temp_str)

            category.sort = 0
            category.is_delete = False
            category.is_enable = True
            category.delete_time = None

            category.save()
            time.sleep(0.05)
        # """
        return HttpResponse(request)


class ImportProductsView(APIView):
    """
    批量导入商品数据
    """
    def get(self, request):
        import_multi_products('\\initial_data\\initial_products.xls')
        return HttpResponse(request)


class ProductsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    商品列表页
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # 配置分页
    pagination_class = CommenPagination

    # 配置过滤器，过滤器适用于精确匹配的情况
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filter_fields = ('creator',)
    filter_class = ProductFilter

    """
    配置需要搜索的字段
    '^' Starts-with search.
    '=' Exact matches.
    '@' Full-text search. (Currently only supported Django's MySQL backend.)
    '$' Regex search.
    """
    search_fields = ('name', 'brief', 'desc')

    """
    配置排序
    """
    ordering_fields = ['add_time', 'name', 'brand']

    # def get_queryset(self):
    #     creator_id = self.request.query_params.get('creator_id', 0)
    #     queryset = Product.objects.all()
    #     if creator_id != 0:
    #         queryset = queryset.filter(creator=creator_id)
    #     return queryset


class ProductCreateView(CreateAPIView):
    """
    创建商品
    """
    pass


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    商品分类列表数据
    """
    queryset = Category.objects.filter(level=1)
    serializer_class = CategorySerializer

