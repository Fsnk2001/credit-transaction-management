from threading import local

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from ..users.models import User
from .models import TransactionType, Transaction, StatusType, DepositCredit, TransferCredit

_signal_processing = local()


@receiver(post_save, sender=DepositCredit)
def update_user_balance_after_deposit_request(sender, instance, created, **kwargs):
    if getattr(_signal_processing, 'in_signal', False):
        return

    if instance.is_approved:
        with transaction.atomic():
            _signal_processing.in_signal = True

            instance.status = StatusType.DONE

            user = User.objects.get(pk=instance.user.id)
            user.balance += instance.amount
            user.save()

            Transaction.objects.create(
                user=instance.user,
                transaction_type=TransactionType.DEPOSIT,
                amount=instance.amount,
                balance_after_transaction=user.balance,
            )

            instance.save(update_fields=['status'])

            _signal_processing.in_signal = False


@receiver(post_save, sender=TransferCredit)
def update_user_balance_after_transfer(sender, instance, created, **kwargs):
    if getattr(_signal_processing, 'in_signal', False):
        return

    if created:
        with transaction.atomic():
            _signal_processing.in_signal = True

            user = User.objects.get(pk=instance.user.id)
            if instance.amount > user.balance:
                instance.status = StatusType.FAILED
            else:
                instance.status = StatusType.DONE

                user.balance -= instance.amount
                user.save()

                Transaction.objects.create(
                    user=instance.user,
                    transaction_type=TransactionType.TRANSFER,
                    amount=instance.amount,
                    balance_after_transaction=user.balance,
                )
            instance.save(update_fields=['status'])

            _signal_processing.in_signal = False
