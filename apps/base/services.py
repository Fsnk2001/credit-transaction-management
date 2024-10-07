from abc import ABC
from typing import Type

from .models import BaseModel
from .repositories import BaseRepository
from .exceptions import NotFoundError


class BaseService(ABC):
    _repository: BaseRepository = None

    @classmethod
    def get_repository(cls) -> BaseRepository:
        return cls._repository

    @classmethod
    def set_filters(cls, params):
        cls.get_repository().set_filters(params)

    @classmethod
    def get_all(cls):
        return cls.get_repository().get_all()

    @classmethod
    def get_by_id(cls, id: int | str):
        return cls.get_repository().get_by_id(id)

    @classmethod
    def create(cls, data: dict):
        return cls.get_repository().create(data)

    @classmethod
    def update(cls, id: int | str, data: dict):
        instance = cls.get_by_id(id)
        return cls.get_repository().update(instance, data)

    @classmethod
    def delete(cls, id: int | str):
        instance = cls.get_by_id(id)
        cls.get_repository().delete(instance)

    @classmethod
    def check_related_user_id(cls, id: int, user_id: int):
        cls.get_repository().check_related_user_id(id, user_id)
