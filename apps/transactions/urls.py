from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TransactionViewSet, IncreaseCreditRequestViewSet

router = DefaultRouter()
router.register(r'', TransactionViewSet, basename='transactions')
router.register(r'increase-credit-requests', IncreaseCreditRequestViewSet, basename='increase-credit-requests')
urlpatterns = [
    path('', include(router.urls)),
]
