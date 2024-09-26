from ..base.repositories import BaseRepository
from .models import User
from .serializers import UserSerializer


class UserRepository(BaseRepository):
    _model = User
    _serializer = UserSerializer
