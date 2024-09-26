from abc import ABC

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
        cls._repository.set_filters(params)

    @classmethod
    def get_all(cls) -> BaseModel:
        return cls._repository.get_all()

    @classmethod
    def get_by_id(cls, id: int | str) -> BaseModel:
        instance = cls._repository.get_by_id(id)
        if instance is None:
            raise NotFoundError()
        return instance

    @classmethod
    def create(cls, data: dict) -> BaseModel:
        return cls._repository.create(data)

    @classmethod
    def update(cls, id: int | str, data: dict) -> BaseModel:
        instance = cls.get_by_id(id)
        return cls._repository.update(instance, data)

    @classmethod
    def delete(cls, id: int | str) -> None:
        instance = cls.get_by_id(id)
        cls._repository.delete(instance)
