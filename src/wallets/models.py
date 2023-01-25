from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from model_utils.models import TimeStampedModel, SoftDeletableModel


User = get_user_model()


class Wallet(TimeStampedModel, SoftDeletableModel):
    user = models.OneToOneField(to=User, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True)
    balance = models.DecimalField(
        verbose_name='Остаток на счёте',
        max_digits=9,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0,
    )
    fixed_price = models.DecimalField(
        verbose_name='Стоимость работы',
        max_digits=9,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0,
        help_text='Фиксирования цена за единицу выполненной работы',
    )

    class Meta:
        verbose_name = 'Кошелёк'
        verbose_name_plural = 'Кошельки пользователей'
        default_related_name = 'wallet'

    def __str__(self) -> str:
        return f'Wallet({self.user=}, {self.balance=}, {self.fixed_price=})'

    def transfer_amount(self) -> None:
        self.balance = models.F('balance') + models.F('fixed_price')
