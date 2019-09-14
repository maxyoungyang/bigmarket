from .models import Region, ShippingInfo, LogisticsCompany, ExpressFeeGroup, ExpressFeeRecord, TrackingNumber, \
    TrackingRecord
from rest_framework.serializers import ModelSerializer


class RegionSerializer(ModelSerializer):

    class Meta:
        model = Region
        field = '__all__'


class ShippingInfoSerializer(ModelSerializer):
    class Meta:
        model = ShippingInfo
        field = '__all__'


class LogisticsCompanySerializer(ModelSerializer):
    class Meta:
        model = LogisticsCompany
        field = '__all__'


class ExpressFeeGroupSerializer(ModelSerializer):
    class Meta:
        model = ExpressFeeGroup
        field = '__all__'


class ExpressFeeRecordSerializer(ModelSerializer):
    class Meta:
        model = ExpressFeeRecord
        field = '__all__'


class TrackingNumberSerializer(ModelSerializer):
    class Meta:
        model = TrackingNumber
        field = '__all__'


class TrackingRecordSerializer(ModelSerializer):
    class Meta:
        model = TrackingRecord
        field = '__all__'

