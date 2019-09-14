from .models import Order, OrderRecord, AfterSalesRecord, OrderStatusHistory, AfterSalesStatusHistory
from rest_framework.serializers import ModelSerializer


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        field = '__all__'


class OrderRecordSerializer(ModelSerializer):
    class Meta:
        model = OrderRecord
        field = '__all__'


class AfterSalesRecordSerializer(ModelSerializer):
    class Meta:
        model = AfterSalesRecord
        field = '__all__'


class OrderStatusHistorySerializer(ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        field = '__all__'


class AfterSalesStatusHistorySerializer(ModelSerializer):
    class Meta:
        model = AfterSalesStatusHistory
        field = '__all__'
