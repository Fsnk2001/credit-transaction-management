from rest_framework.permissions import BasePermission


class IsAdminPermission(BasePermission):
    message = "Permission denied, you are not admin."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)


class IsSellerPermission(BasePermission):
    message = "Permission denied, you are not seller."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_seller)


class IsAdminOrSellerPermission(BasePermission):
    message = "Permission denied. You must be either an admin or a seller."

    def has_permission(self, request, view):
        is_admin = IsAdminPermission().has_permission(request, view)
        is_seller = IsSellerPermission().has_permission(request, view)
        return is_admin or is_seller
