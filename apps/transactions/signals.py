from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from ..users.models import User
from .models import TransactionType, Transaction, IncreaseCreditRequest


@receiver(post_save, sender=IncreaseCreditRequest)
def update_user_balance_after_increase_credit_request(sender, instance, created, **kwargs):
    if instance.is_approved:
        with transaction.atomic():
            user = User.objects.get(pk=instance.user)
            user.balance += instance.amount
            user.save()

            Transaction.objects.create(
                user=instance.user,
                transaction_type=TransactionType.INCREASE,
                amount=instance.amount,
                balance_after_transaction=user.balance,
            )
