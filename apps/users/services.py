from ..base.services import BaseService
from .repositories import UserRepository


class UserService(BaseService):
    _repository = UserRepository
