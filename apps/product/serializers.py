from rest_framework.serializers import ModelSerializer
from .models import Product, ProductSalesType, Spec, SpecDetail, \
    AvailableSpec, Brand, Category, InteractedProduct, InventoryHistory, BrandCategory


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


class SubCategorySerializer3(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer2(ModelSerializer):
    sub_categories = SubCategorySerializer3(many=True)
    class Meta:
        model = Category
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    sub_categories = SubCategorySerializer2(many=True)
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


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class BrandCategorySerializer(ModelSerializer):
    class Meta:
        model = BrandCategory
        fields = '__all__'