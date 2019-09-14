from .models import TransactionRecord
from rest_framework.serializers import ModelSerializer


class TransactionRecordSerializer(ModelSerializer):

    class Meta:
        model = TransactionRecord
        field = '__all__'
