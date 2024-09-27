from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from ..base.views import BaseViewSet
from ..base.responses import Response
from ..base.permissions import IsAdminPermission, IsSellerPermission
from .serializers import WalletSerializer
from .services import WalletService


class WalletViewSet(BaseViewSet):
    _service = WalletService
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminPermission]
        self.check_permissions(request)

        data = self._service.get_all()
        return Response(
            data={
                "wallets": self.get_serializer(data, many=True).data
            }, message="List of wallets.", meta={}
        )

    @action(detail=False, methods=['get'], url_path='me')
    def get_me(self, request, *args, **kwargs):
        user_id = request.user.id
        data = self._service.get_by_id(user_id)
        return Response(
            data={
                "wallet": self.get_serializer(data).data
            }, message="The wallet.", meta={}
        )

    def retrieve(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminPermission]
        self.check_permissions(request)

        id = kwargs.get('pk')
        data = self._service.get_by_id(id)
        return Response(
            data={
                "wallet": self.get_serializer(data).data
            }, message="The wallet.", meta={}
        )

    def create(self, request, *args, **kwargs):
        user = self._service.create(request.data)
        return Response(
            data={
                "wallet": self.get_serializer(user).data
            }, message="Wallet created successfully.", status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        updated_user = self._service.update(id, request.data)
        return Response(
            data={
                "wallet": self.get_serializer(updated_user).data
            }, message="Wallet updated successfully.", status=status.HTTP_200_OK
        )
