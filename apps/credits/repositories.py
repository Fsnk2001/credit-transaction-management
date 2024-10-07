from django.db import transaction
from django.db.models import QuerySet
from django.utils import timezone

from ..base.repositories import BaseRepository
from ..base.exceptions import NotFoundError, ValidationError
from .models import Transaction, DepositCredit, TransferCredit, StatusType
from .serializers import TransactionSerializer, DepositCreditSerializer, TransferCreditSerializer


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

    @classmethod
    def update_deposit_if_not_approved(cls, id: int, data: dict):
        with transaction.atomic():
            deposit = cls._model.objects.select_for_update().filter(pk=id).first()
            if deposit is None:
                raise NotFoundError()

            if deposit.status == StatusType.DONE:
                raise ValidationError("You cannot update because it is already done.")

            return cls.update(deposit, data)

    @classmethod
    def approve_or_deny_deposit(cls, id: int, modified_by_id: int, data: dict):
        with transaction.atomic():
            deposit = cls._model.objects.select_for_update().filter(pk=id).first()
            if deposit is None:
                raise NotFoundError()

            if deposit.status == StatusType.DONE:
                raise ValidationError("This deposit has already been modified.")

            data.update({
                'modified_by': modified_by_id,
            })
            return cls.update(deposit, data)


class TransferCreditRepository(BaseRepository):
    _model = TransferCredit
    _serializer = TransferCreditSerializer

    @classmethod
    def get_transfers_based_on_user_id(cls, user_id: int) -> QuerySet:
        queryset = cls.get_queryset()
        return queryset.filter(user_id=user_id).all()
