from .models import Pricing, TieredPricing, StepPrice
from rest_framework.serializers import ModelSerializer


class PricingSerializer(ModelSerializer):
    class Meta:
        model = Pricing
        field = '__all__'


class TieredPricingSerializer(ModelSerializer):
    class Meta:
        model = TieredPricing
        field = '__all__'


class StepPriceSerializer(ModelSerializer):
    class Meta:
        model = StepPrice
        field = '__all__'
