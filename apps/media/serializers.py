from .models import ProductMedia, ArticlesMedia, SystemMedia
from rest_framework.serializers import ModelSerializer


class ProductMediaSerializer(ModelSerializer):
    class Meta:
        model = ProductMedia
        field = '__all__'


class ArticlesMediaSerializer(ModelSerializer):
    class Meta:
        model = ArticlesMedia
        field = '__all__'


class SystemMediaSerializer(ModelSerializer):
    class Meta:
        model = SystemMedia
        field = '__all__'
