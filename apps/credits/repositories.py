from django.db.models import QuerySet

from ..base.repositories import BaseRepository
from .models import Transaction, DepositCreditRequest
from .serializers import TransactionSerializer, DepositCreditRequestSerializer


class TransactionRepository(BaseRepository):
    _model = Transaction
    _serializer = TransactionSerializer

    @classmethod
    def get_transactions_based_on_user_id(cls, user_id: int) -> QuerySet:
        queryset = cls.get_queryset()
        return queryset.filter(user_id=user_id).all()


class DepositCreditRequestRepository(BaseRepository):
    _model = DepositCreditRequest
    _serializer = DepositCreditRequestSerializer

    @classmethod
    def get_deposit_requests_based_on_user_id(cls, user_id: int) -> QuerySet:
        queryset = cls.get_queryset()
        return queryset.filter(user_id=user_id).all()
