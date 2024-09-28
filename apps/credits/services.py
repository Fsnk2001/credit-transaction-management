from django.utils import timezone

from ..base.services import BaseService
from ..base.exceptions import ValidationError, PermissionDeniedError
from .repositories import TransactionRepository, DepositCreditRequestRepository


class TransactionService(BaseService):
    _repository = TransactionRepository

    @classmethod
    def get_my_transactions(cls, user_id: int):
        return list(cls._repository.get_transactions_based_on_user_id(user_id))


class DepositCreditRequestService(BaseService):
    _repository = DepositCreditRequestRepository
    transaction_service = TransactionService

    @classmethod
    def create_request(cls, user_id: id, data: dict):
        data.update({
            "user": user_id}
        )
        return cls.create(data)

    @classmethod
    def is_request_yours(cls, id: int, user_id: int):
        deposit_request = cls.get_by_id(id)
        if deposit_request.user_id != user_id:
            raise PermissionDeniedError()

    @classmethod
    def get_my_deposit_requests(cls, user_id: int):
        return list(cls._repository.get_deposit_requests_based_on_user_id(user_id))

    @classmethod
    def update_request_if_not_approved(cls, id: int, data: dict):
        deposit_request = cls.select_for_update_by_id(id)
        if deposit_request.is_verfied:
            raise ValidationError("You cannot update because it is already approved.")
        return cls.update(id, data)

    @classmethod
    def approve(cls, id: int, approved_by_id: int, data: dict):
        deposit_request = cls.select_for_update_by_id(id)
        if deposit_request.is_verfied:
            raise ValidationError("This request has already been approved.")

        data.update({
            'approved_by': approved_by_id,
            'approved_at': timezone.now()
        })
        return cls.update(id, data)
