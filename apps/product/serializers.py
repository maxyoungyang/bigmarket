from rest_framework.serializers import ModelSerializer
from .models import Product, ProductSalesType, Spec, SpecDetail,\
    AvailableSpec, Brand, Category, InteractedProduct, InventoryHistory


class PorductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductSalesTypeSerializer(ModelSerializer):
    class Meta:
        model = ProductSalesType
        fields = '__all__'


class SpecSerializer(ModelSerializer):
    class Meta:
        model = Spec
        fields = '__all__'


class SpecDetailSerializer(ModelSerializer):
    class Meta:
        model = SpecDetail
        fields = '__all__'


class AvailableSpecSerializer(ModelSerializer):
    class Meta:
        model = AvailableSpec
        fields = '__all__'


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class InteractedProductSerializer(ModelSerializer):

    class Meta:
        model = InteractedProduct
        fields = '__all__'


class InventoryHistorySerializer(ModelSerializer):

    class Meta:
        model = InventoryHistory
        fields = '__all__'