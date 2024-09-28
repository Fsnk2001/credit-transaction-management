from rest_framework import serializers

from ..base.serializers import BaseModelSerializer
from ..users.models import User, UserRoles
from .models import TransactionType, Transaction, DepositCreditRequest


class TransactionSerializer(BaseModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class DepositCreditRequestSerializer(BaseModelSerializer):
    class Meta:
        model = DepositCreditRequest
        fields = '__all__'

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    amount = serializers.IntegerField(min_value=1)
    is_approved = serializers.BooleanField(default=False, required=False)
    approved_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, required=False)
    approved_at = serializers.DateTimeField(allow_null=True, required=False)

    def validate_user(self, value):
        if not value.has_role(UserRoles.SELLER):
            raise serializers.ValidationError("The user must have the role of seller.")
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("The amount must be greater than 0.")
        return value

    def validate_approved_by(self, value):
        if not value.has_role(UserRoles.ADMIN):
            raise serializers.ValidationError("The user must have the role of admin.")
        return value


class CreateOrUpdateDepositCreditRequestSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)


class ApproveDepositCreditRequestSerializer(serializers.Serializer):
    is_approved = serializers.BooleanField(default=False)
