from rest_framework import serializers
from account.serializers import UserSerializer
from .models import TransactionInvoice,TransactionRecord

class TransactionHistorySerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=TransactionRecord
        fields="__all__"
        depth=1


class TransactionHistorySerializerDeatils(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=TransactionRecord
        fields="__all__"
        depth=1