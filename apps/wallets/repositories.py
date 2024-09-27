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
