from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from .models import Wallet, WalletTransaction, IncreaseCreditRequest


@receiver(post_save, sender=IncreaseCreditRequest)
def update_wallet_balance(sender, instance, created, **kwargs):
    # Check if the increase credit request was approved
    if instance.is_approved:
        with transaction.atomic():
            # Get or create the wallet for the user
            wallet, created = Wallet.objects.get_or_create(user=instance.user)
            # Update the wallet balance
            wallet.balance += instance.amount
            wallet.save()
