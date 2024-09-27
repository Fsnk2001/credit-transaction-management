from django.db.models import QuerySet

from ..base.repositories import BaseRepository
from .models import Wallet, WalletTransaction, IncreaseCreditRequest
from .serializers import WalletSerializer, WalletTransactionSerializer, IncreaseCreditRequestSerializer


class WalletRepository(BaseRepository):
    _model = Wallet
    _serializer = WalletSerializer


class WalletTransactionRepository(BaseRepository):
    _model = WalletTransaction
    _serializer = WalletTransactionSerializer


class IncreaseCreditRequestRepository(BaseRepository):
    _model = IncreaseCreditRequest
    _serializer = IncreaseCreditRequestSerializer

    @classmethod
    def get_increase_credit_requests_based_on_user_id(cls, user_id: int) -> QuerySet:
        queryset = cls.get_queryset()
        return queryset.filter(user_id=user_id).all()
