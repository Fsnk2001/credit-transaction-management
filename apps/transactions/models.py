from django.db import models

from ..base.models import BaseModel
from ..users.models import User


class TransactionType(models.TextChoices):
    INCREASE = 'increase', 'Increase'
    DECREASE = 'decrease', 'Decrease'


class Transaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    transaction_type = models.CharField(max_length=50, choices=TransactionType.choices)
    amount = models.PositiveBigIntegerField()
    balance_after_transaction = models.PositiveBigIntegerField()


class IncreaseCreditRequest(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    amount = models.PositiveBigIntegerField()
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='request_approvals')
    approved_at = models.DateTimeField(null=True, blank=True)
