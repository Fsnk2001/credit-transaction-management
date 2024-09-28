from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from ..users.models import User
from .models import Transaction, IncreaseCreditRequest


@receiver(post_save, sender=IncreaseCreditRequest)
def update_wallet_balance(sender, instance, created, **kwargs):
    if instance.is_approved:
        with transaction.atomic():
            user = User.objects.get(pk=instance.user)
            user.balance += instance.amount
            user.save()
