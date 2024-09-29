from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from ..base.views import BaseViewSet
from ..base.responses import Response
from ..base.permissions import IsAdminPermission, IsSellerPermission
from .serializers import (
    TransactionSerializer,
    DepositCreditSerializer,
    CreateOrUpdateDepositCreditSerializer,
    ApproveDepositCreditSerializer,
    TransferCreditSerializer,
    CreateTransferCreditSerializer,
)
from .services import TransactionService, DepositCreditService, TransferCreditService


class TransactionViewSet(BaseViewSet):
    _service = TransactionService
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminPermission]
        self.check_permissions(request)

        data = self._service.get_all()
        return Response(
            data={
                "transactions": self.get_serializer(data, many=True).data
            }, message="List of transactions.", meta={}
        )

    @action(detail=False, methods=['get'], url_path='me')
    def get_me(self, request, *args, **kwargs):
        user_id = request.user.id
        data = self._service.get_my_transactions(user_id)
        return Response(
            data={
                "transaction": self.get_serializer(data).data
            }, message="The transaction.", meta={}
        )

    def retrieve(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminPermission]
        self.check_permissions(request)

        id = kwargs.get('pk')
        data = self._service.get_by_id(id)
        return Response(
            data={
                "transaction": self.get_serializer(data).data
            }, message="The transaction.", meta={}
        )


class DepositCreditViewSet(BaseViewSet):
    _service = DepositCreditService
    serializer_class = DepositCreditSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminPermission]
        self.check_permissions(request)

        deposits = self._service.get_all()
        return Response(
            data={
                "deposits": self.get_serializer(deposits, many=True).data
            }, message="List of deposits.", meta={}
        )

    @action(detail=False, methods=['get'], url_path='me')
    def get_me(self, request, *args, **kwargs):
        self.permission_classes = [IsSellerPermission]
        self.check_permissions(request)

        user_id = request.user.id
        deposits = self._service.get_my_deposits(user_id)
        return Response(
            data={
                "deposits": self.get_serializer(deposits, many=True).data
            }, message="Your deposits.", meta={}
        )

    def retrieve(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminPermission]
        self.check_permissions(request)

        id = kwargs.get('pk')
        deposit = self._service.get_by_id(id)
        return Response(
            data={
                "deposit": self.get_serializer(deposit).data
            }, message="The deposit.", meta={}
        )

    def create(self, request, *args, **kwargs):
        user_id = request.user.id
        serializer = CreateOrUpdateDepositCreditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        deposit = self._service.create_deposit(user_id, request.data)
        return Response(
            data={
                "deposit": self.get_serializer(deposit).data
            }, message="Deposit created successfully.", status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        user_id = request.user.id
        self._service.check_related_user_id(id, user_id)

        serializer = CreateOrUpdateDepositCreditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_deposit = self._service.update_deposit_if_not_approved(id, serializer.validated_data)
        return Response(
            data={
                "deposit": self.get_serializer(updated_deposit).data
            }, message="Deposit updated successfully.", status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def approve(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminPermission]
        self.check_permissions(request)

        id = kwargs.get('pk')
        user_id = request.user.id
        serializer = ApproveDepositCreditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_deposit = self._service.approve_deposit(id, user_id, serializer.validated_data)
        return Response(
            data={
                "deposit": self.get_serializer(updated_deposit).data
            }, message="Deposit approved successfully.", status=status.HTTP_200_OK
        )


class TransferCreditViewSet(BaseViewSet):
    _service = TransferCreditService
    serializer_class = TransferCreditSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminPermission]
        self.check_permissions(request)

        transfers = self._service.get_all()
        return Response(
            data={
                "transfers": self.get_serializer(transfers, many=True).data
            }, message="List of transfers.", meta={}
        )

    @action(detail=False, methods=['get'], url_path='me')
    def get_me(self, request, *args, **kwargs):
        self.permission_classes = [IsSellerPermission]
        self.check_permissions(request)

        user_id = request.user.id
        transfers = self._service.get_my_transfers(user_id)
        return Response(
            data={
                "transfers": self.get_serializer(transfers, many=True).data
            }, message="Your transfers.", meta={}
        )

    def retrieve(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminPermission]
        self.check_permissions(request)

        id = kwargs.get('pk')
        transfer = self._service.get_by_id(id)
        return Response(
            data={
                "transfer": self.get_serializer(transfer).data
            }, message="The transfer.", meta={}
        )

    def create(self, request, *args, **kwargs):
        user_id = request.user.id
        serializer = CreateTransferCreditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transfer = self._service.create_transfer(user_id, request.data)
        return Response(
            data={
                "transfer": self.get_serializer(transfer).data
            }, message="Transfer created successfully.", status=status.HTTP_201_CREATED
        )
