from django.db import models

from ..base.models import BaseModel

from ..users.models import User


class Wallet(BaseModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    balance = models.PositiveBigIntegerField(default=0)


class TransactionType(models.TextChoices):
    INCREASE = 'increase', 'Increase'
    DECREASE = 'decrease', 'Decrease'


class WalletTransaction(BaseModel):
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    transaction_type = models.CharField(max_length=50, choices=TransactionType.choices)
    amount = models.PositiveBigIntegerField()


class IncreaseCreditRequest(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    amount = models.PositiveBigIntegerField()
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='request_approvals')
    approved_at = models.DateTimeField(null=True, blank=True)
