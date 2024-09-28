from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TransactionViewSet, DepositCreditRequestViewSet

router = DefaultRouter()
router.register(r'deposits', DepositCreditRequestViewSet, basename='deposits')
router.register(r'transactions', TransactionViewSet, basename='transactions')
urlpatterns = [
    path('', include(router.urls)),
]
