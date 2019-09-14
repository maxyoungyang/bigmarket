from .models import Promotion
from rest_framework.serializers import ModelSerializer


class PromotionSerializer(ModelSerializer):
    class Meta:
        model = Promotion
        field = '__all__'
