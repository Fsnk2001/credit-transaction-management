from ..base.services import BaseService
from .repositories import WalletRepository, WalletTransactionRepository, IncreaseCreditRequestRepository


class WalletService(BaseService):
    _repository = WalletRepository


class WalletTransactionService(BaseService):
    _repository = WalletTransactionRepository


class IncreaseCreditRequestService(BaseService):
    _repository = IncreaseCreditRequestRepository
