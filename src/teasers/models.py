from django.contrib.auth import get_user_model
from django.db import models

from model_utils.models import TimeStampedModel
from model_utils import Choices

FIRST_CHARACTERS = 15

User = get_user_model()

PAID = ('paid', 'Оплачено')
REFUSAL = ('refusal', 'Отказ')
UNDEFINED = ('undefined', 'Не определён')


class BaseTitleModel(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=64)
    description = models.TextField(verbose_name='Описание', blank=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel, BaseTitleModel):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)
        constraints = [models.UniqueConstraint(fields=('title',), name='unique_category')]

    def __str__(self) -> str:
        return f'Category({self.title=}, {self.description[:FIRST_CHARACTERS]=})'


class Teaser(TimeStampedModel, BaseTitleModel):
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name='Категория')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Автор')
    STATUS = Choices(PAID, REFUSAL, UNDEFINED)
    status = models.CharField(choices=STATUS, default=STATUS.undefined, max_length=20)

    class Meta:
        verbose_name = 'Тизер'
        verbose_name_plural = 'Тизеры'
        ordering = ('title',)
        default_related_name = 'teasers'
        constraints = [models.UniqueConstraint(fields=('title', 'user'), name='unique_teaser')]
        indexes = [
            models.Index(fields=('title',), name='index_teaser_title'),
            models.Index(fields=('status',), name='index_teaser_status')
        ]

    def __str__(self) -> str:
        return f'Teaser({self.title=}, {self.status=}, {self.description[:FIRST_CHARACTERS]=})'
