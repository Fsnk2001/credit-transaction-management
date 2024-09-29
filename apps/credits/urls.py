from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TransactionViewSet, DepositCreditViewSet, TransferCreditViewSet

router = DefaultRouter()
router.register(r'deposits', DepositCreditViewSet, basename='deposits')
router.register(r'transfers', TransferCreditViewSet, basename='transfers')
router.register(r'transactions', TransactionViewSet, basename='transactions')
urlpatterns = [
    path('', include(router.urls)),
]
