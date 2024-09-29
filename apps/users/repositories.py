from ..base.repositories import BaseRepository
from .models import User, PhoneNumber
from .serializers import UserSerializer, PhoneNumberSerializer


class UserRepository(BaseRepository):
    _model = User
    _serializer = UserSerializer

    @classmethod
    def change_password(cls, instance: User, password: str):
        instance.set_password(password)
        instance.save()
        return instance


class PhoneNumberRepository(BaseRepository):
    _model = PhoneNumber
    _serializer = PhoneNumberSerializer
