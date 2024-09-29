from django.utils import timezone

from .repositories import TransactionRepository, DepositCreditRepository, TransferCreditRepository
from ..base.exceptions import ValidationError, PermissionDeniedError
from ..base.services import BaseService


class TransactionService(BaseService):
    _repository = TransactionRepository

    @classmethod
    def get_my_transactions(cls, user_id: int):
        return cls._repository.get_transactions_based_on_user_id(user_id)


class DepositCreditService(BaseService):
    _repository = DepositCreditRepository
    transaction_service = TransactionService

    @classmethod
    def create_deposit(cls, user_id: id, data: dict):
        data.update({
            "user": user_id}
        )
        return cls.create(data)

    @classmethod
    def get_my_deposits(cls, user_id: int):
        return cls._repository.get_deposits_based_on_user_id(user_id)

    @classmethod
    def update_deposit_if_not_approved(cls, id: int, data: dict):
        return cls._repository.update_deposit_if_not_approved(id, data)

    @classmethod
    def approve_deposit(cls, id: int, approved_by_id: int, data: dict):
        return cls._repository.approve_deposit(id, approved_by_id, data)


class TransferCreditService(BaseService):
    _repository = TransferCreditRepository
    transaction_service = TransactionService

    @classmethod
    def create_transfer(cls, user_id: id, data: dict):
        data.update({
            "user": user_id}
        )
        return cls.create(data)

    @classmethod
    def get_my_transfers(cls, user_id: int):
        return cls._repository.get_transfers_based_on_user_id(user_id)
