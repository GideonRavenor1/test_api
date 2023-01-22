from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils import Choices

ADMIN = ('admin', 'Админ')
AUTHOR = ('author', 'Автор')


class User(AbstractUser):
    STATUS = Choices(ADMIN, AUTHOR)
    role = models.CharField(verbose_name='Роль', max_length=20, choices=STATUS, default=STATUS.author)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
        indexes = [
            models.Index(fields=('role',), name='index_user_role'),
        ]

    def __str__(self) -> str:
        return f'User(username={self.get_username()}, {self.role=})'

    @property
    def is_author(self) -> bool:
        return self.role == self.STATUS.author

    @property
    def is_admin(self) -> bool:
        return self.role == self.STATUS.admin
