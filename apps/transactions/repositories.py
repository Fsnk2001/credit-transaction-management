from django.db.models import QuerySet

from ..base.repositories import BaseRepository
from .models import Transaction, IncreaseCreditRequest
from .serializers import TransactionSerializer, IncreaseCreditRequestSerializer


class TransactionRepository(BaseRepository):
    _model = Transaction
    _serializer = TransactionSerializer

    @classmethod
    def get_transactions_based_on_user_id(cls, user_id: int) -> QuerySet:
        queryset = cls.get_queryset()
        return queryset.filter(user_id=user_id).all()


class IncreaseCreditRequestRepository(BaseRepository):
    _model = IncreaseCreditRequest
    _serializer = IncreaseCreditRequestSerializer

    @classmethod
    def get_increase_credit_requests_based_on_user_id(cls, user_id: int) -> QuerySet:
        queryset = cls.get_queryset()
        return queryset.filter(user_id=user_id).all()
