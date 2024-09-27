from rest_framework import serializers

from ..base.serializers import BaseModelSerializer
from .models import Wallet, TransactionType, WalletTransaction, IncreaseCreditRequest


class WalletSerializer(BaseModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class WalletTransactionSerializer(BaseModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = '__all__'


class IncreaseCreditRequestSerializer(BaseModelSerializer):
    class Meta:
        model = IncreaseCreditRequest
        fields = '__all__'
