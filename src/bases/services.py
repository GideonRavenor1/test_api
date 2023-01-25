from abc import ABC, abstractmethod

from django.db.models import Model


class BaseServices(ABC):

    @abstractmethod
    def __call__(self) -> list[Model]:
        raise NotImplementedError
