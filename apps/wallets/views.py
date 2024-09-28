from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from ..base.views import BaseViewSet
from ..base.responses import Response
from ..base.permissions import IsAdminPermission, IsSellerPermission
from .serializers import (
    WalletSerializer,
    IncreaseCreditRequestSerializer,
    CreateOrUpdateIncreaseCreditRequestSerializer,
    ApproveIncreaseCreditRequestSerializer,
)
from .services import WalletService, IncreaseCreditRequestService


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
        wallet = self._service.create(request.data)
        return Response(
            data={
                "wallet": self.get_serializer(wallet).data
            }, message="Wallet created successfully.", status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        updated_wallet = self._service.update(id, request.data)
        return Response(
            data={
                "wallet": self.get_serializer(updated_wallet).data
            }, message="Wallet updated successfully.", status=status.HTTP_200_OK
        )


class IncreaseCreditRequestViewSet(BaseViewSet):
    _service = IncreaseCreditRequestService
    serializer_class = IncreaseCreditRequestSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminPermission]
        self.check_permissions(request)

        data = self._service.get_all()
        return Response(
            data={
                "credit_requests": self.get_serializer(data, many=True).data
            }, message="List of credit requests.", meta={}
        )

    @action(detail=False, methods=['get'], url_path='me')
    def get_me(self, request, *args, **kwargs):
        self.permission_classes = [IsSellerPermission]
        self.check_permissions(request)

        user_id = request.user.id
        data = self._service.get_my_increase_credit_requests(user_id)
        return Response(
            data={
                "credit_requests": self.get_serializer(data).data
            }, message="Your credit requests.", meta={}
        )

    def retrieve(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminPermission]
        self.check_permissions(request)

        id = kwargs.get('pk')
        data = self._service.get_by_id(id)
        return Response(
            data={
                "credit_request": self.get_serializer(data).data
            }, message="The credit request.", meta={}
        )

    def create(self, request, *args, **kwargs):
        user_id = request.user.id
        serializer = CreateOrUpdateIncreaseCreditRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        credit_request = self._service.create_request(user_id, serializer.validated_data)
        return Response(
            data={
                "credit_request": self.get_serializer(credit_request).data
            }, message="Increase credit request created successfully.", status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        user_id = request.user.id
        self._service.is_request_yours(id, user_id)

        serializer = CreateOrUpdateIncreaseCreditRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_credit_request = self._service.update_request_if_not_approved(id, serializer.validated_data)
        return Response(
            data={
                "credit_request": self.get_serializer(updated_credit_request).data
            }, message="Increase credit request updated successfully.", status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def approve(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminPermission]
        self.check_permissions(request)

        id = kwargs.get('pk')
        user_id = request.user.id
        serializer = ApproveIncreaseCreditRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_credit_request = self._service.approve(id, user_id, serializer.validated_data)
        return Response(
            data={
                "credit_request": self.get_serializer(updated_credit_request).data
            }, message="Increase credit request approved successfully.", status=status.HTTP_200_OK
        )
