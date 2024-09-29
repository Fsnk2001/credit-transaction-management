from django.db import models


class UserRoles(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    SELLER = 'seller', 'Seller'
