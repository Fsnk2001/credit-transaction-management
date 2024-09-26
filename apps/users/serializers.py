from rest_framework import serializers

from ..base.serializers import BaseModelSerializer
from ..base.serializer_fields import PasswordField
from .models import UserRoles, User


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_active', 'password', 'confirm_password')
        read_only_fields = ('is_superuser', 'is_admin', 'is_seller')

    username = serializers.CharField(max_length=255)
    password = PasswordField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already taken.")
        return username

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please fill password and confirm password.")

        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Confirm password is not equal to password.")

        data.pop('confirm_password', None)
        return data
