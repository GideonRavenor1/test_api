from typing import Type

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from src.wallets.models import Wallet

User = get_user_model()


@receiver(post_save, sender=User)
def initial_user_data(sender: Type[User], instance: User, created: bool = False, **kwargs) -> None:
    if created:
        Token.objects.create(user=instance)
        Wallet.objects.create(user=instance)
