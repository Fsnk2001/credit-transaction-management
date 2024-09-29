from django.db import models

from ..base.models import BaseModel
from ..users.models import User, PhoneNumber


class TransactionType(models.TextChoices):
    DEPOSIT = 'deposit', 'Deposit'
    TRANSFER = 'transfer', 'Transfer'


class Transaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    transaction_type = models.CharField(max_length=50, choices=TransactionType.choices)
    amount = models.PositiveBigIntegerField()
    balance_after_transaction = models.PositiveBigIntegerField()


class StatusType(models.TextChoices):
    PENDING = 'pending', 'Pending'
    DONE = 'done', 'Done'
    FAILED = 'failed', 'Failed'


class DepositCredit(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    amount = models.PositiveBigIntegerField()
    is_approved = models.BooleanField(default=False)
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='deposit_modifications', null=True)
    status = models.CharField(max_length=20, choices=StatusType.choices, default=StatusType.PENDING)


class TransferCredit(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.PROTECT)
    amount = models.PositiveBigIntegerField()
    status = models.CharField(max_length=20, choices=StatusType.choices, default=StatusType.PENDING)
