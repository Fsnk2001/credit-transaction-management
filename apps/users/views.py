from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from ..base.views import BaseViewSet
from ..base.responses import Response
from ..base.permissions import IsAdminPermission, IsSellerPermission, IsAdminOrSellerPermission
from .serializers import (
    UserSerializer,
    UpdateUserSerializer,
    ResetPasswordSerializer,
    PhoneNumberSerializer,
)
from .services import UserService, PhoneNumberService


class UserViewSet(BaseViewSet):
    _service = UserService
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminPermission]
        self.check_permissions(request)

        users = self._service.get_all()
        return Response(
            data={
                "users": self.get_serializer(users, many=True).data
            }, message="List of users.", meta={}
        )

    @action(detail=False, methods=['get'], url_path='me')
    def get_me(self, request, *args, **kwargs):
        user_id = request.user.id
        user = self._service.get_by_id(user_id)
        return Response(
            data={
                "user": self.get_serializer(user).data
            }, message="The user.", meta={}
        )

    def retrieve(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminPermission]
        self.check_permissions(request)

        id = kwargs.get('pk')
        user = self._service.get_by_id(id)
        return Response(
            data={
                "user": self.get_serializer(user).data
            }, message="The user.", meta={}
        )

    def create(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminPermission]
        self.check_permissions(request)

        user = self._service.create(request.data)
        return Response(
            data={
                "user": self.get_serializer(user).data
            }, message="User created successfully.", status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminPermission]
        self.check_permissions(request)

        id = kwargs.get('pk')
        serializer = UpdateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_user = self._service.update(id, request.data)
        return Response(
            data={
                "user": self.get_serializer(updated_user).data
            }, message="User updated successfully.", status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'], url_path='reset-password')
    def reset_password(self, request, *args, **kwargs):
        user_id = request.user.id
        serializer = ResetPasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        user = self._service.reset_password(user_id, serializer.validated_data.get('password'))
        return Response(
            data={
                "user": self.get_serializer(user).data
            }, message="User's password updated successfully.", meta={}
        )


class PhoneNumberViewSet(BaseViewSet):
    _service = PhoneNumberService
    serializer_class = PhoneNumberSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminOrSellerPermission]
        self.check_permissions(request)

        numbers = self._service.get_all()
        return Response(
            data={
                "numbers": self.get_serializer(numbers, many=True).data
            }, message="List of phone numbers.", meta={}
        )

    def retrieve(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminOrSellerPermission]
        self.check_permissions(request)

        id = kwargs.get('pk')
        number = self._service.get_by_id(id)
        return Response(
            data={
                "number": self.get_serializer(number).data
            }, message="The phone number.", meta={}
        )

    def create(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminPermission]
        self.check_permissions(request)

        number = self._service.create(request.data)
        return Response(
            data={
                "number": self.get_serializer(number).data
            }, message="Phone number created successfully.", status=status.HTTP_201_CREATED
        )
