from .models import PaymentMethod, PaymentCompany, FeeRateRecord
from rest_framework.serializers import ModelSerializer


class PaymentMethodSerializer(ModelSerializer):
    class Meta:
        model = PaymentMethod
        field = '__all__'


class PaymentCompanySerializer(ModelSerializer):
    class Meta:
        model = PaymentCompany
        field = '__all__'


class FeeRateRecordSerializer(ModelSerializer):
    class Meta:
        model = FeeRateRecord
        field = '__all__'
