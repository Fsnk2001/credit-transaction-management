from django.utils import timezone

from ..base.models import BaseModel
from ..base.services import BaseService
from ..base.exceptions import ValidationError, PermissionDeniedError
from .repositories import WalletRepository, WalletTransactionRepository, IncreaseCreditRequestRepository


class WalletService(BaseService):
    _repository = WalletRepository


class WalletTransactionService(BaseService):
    _repository = WalletTransactionRepository


class IncreaseCreditRequestService(BaseService):
    _repository = IncreaseCreditRequestRepository
    wallet_service = WalletService
    wallet_transaction_service = WalletTransactionService

    @classmethod
    def create_request(cls, user_id: id, data: dict):
        data.update({
            "user": user_id}
        )
        return cls.create(data)

    @classmethod
    def is_request_yours(cls, id: int, user_id: int):
        credit_request = cls.get_by_id(id)
        if credit_request.user_id != user_id:
            raise PermissionDeniedError()

    @classmethod
    def get_my_increase_credit_requests(cls, user_id: int):
        return list(cls._repository.get_increase_credit_requests_based_on_user_id(user_id))

    @classmethod
    def update_request_if_not_approved(cls, id: int, data: dict):
        credit_request = cls.get_by_id(id)
        if credit_request.is_verfied:
            raise ValidationError("You cannot update because it is already approved.")
        return cls.update(id, data)

    @classmethod
    def approve(cls, id: int, approved_by_id: int, data: dict):
        data.update({
            'approved_by': approved_by_id,
            'approved_at': timezone.now()
        })
        return cls.update(id, data)
