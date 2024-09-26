from abc import ABC
from typing import Type

from django.db.models import QuerySet

from .models import BaseModel
from .serializers import BaseModelSerializer


class BaseRepository(ABC):
    _model: Type[BaseModel] = None
    _serializer: Type[BaseModelSerializer] = None

    @classmethod
    def _get_model(cls) -> Type[BaseModel]:
        return cls._model

    @classmethod
    def _get_serializer(cls) -> Type[BaseModelSerializer]:
        return cls._serializer

    @classmethod
    def get_queryset(cls) -> QuerySet:
        return cls._model.objects.get_queryset()

    @classmethod
    def set_filters(cls, filters):
        pass

    @classmethod
    def get_all(cls) -> BaseModel:
        return cls._model.objects.get_queryset().all()

    @classmethod
    def get_by_id(cls, id: int | str) -> BaseModel:
        return cls._model.objects.filter(pk=id).first()

    @classmethod
    def create(cls, data: dict) -> BaseModel:
        serializer = cls._serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @classmethod
    def update(cls, instance: BaseModel, data: dict) -> BaseModel:
        serializer = cls._serializer(instance=instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @classmethod
    def delete(cls, instance: BaseModel) -> None:
        instance.delete()
