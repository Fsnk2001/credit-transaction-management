from django.db.models import QuerySet

from ..base.repositories import BaseRepository
from .models import Transaction, DepositCredit
from .serializers import TransactionSerializer, DepositCreditSerializer


class TransactionRepository(BaseRepository):
    _model = Transaction
    _serializer = TransactionSerializer

    @classmethod
    def get_transactions_based_on_user_id(cls, user_id: int) -> QuerySet:
        queryset = cls.get_queryset()
        return queryset.filter(user_id=user_id).all()


class DepositCreditRepository(BaseRepository):
    _model = DepositCredit
    _serializer = DepositCreditSerializer

    @classmethod
    def get_deposits_based_on_user_id(cls, user_id: int) -> QuerySet:
        queryset = cls.get_queryset()
        return queryset.filter(user_id=user_id).all()
