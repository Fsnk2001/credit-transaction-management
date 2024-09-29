from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from ..base.serializers import BaseModelSerializer
from ..base.validators import contains_number_validator, contains_letter_validator, contains_special_char_validator, \
    phone_number_validator
from .models import UserRoles, User, PhoneNumber


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_active', 'password', 'confirm_password', 'roles')
        read_only_fields = ('is_superuser', 'is_admin', 'is_seller')

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(min_length=8, write_only=True, validators=[
        contains_number_validator, contains_letter_validator, contains_special_char_validator
    ])
    confirm_password = serializers.CharField(write_only=True)
    roles = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    is_active = serializers.BooleanField(default=True, required=False)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already taken.")
        return username

    def validate_roles(self, value):
        roles = [choice[0] for choice in UserRoles.choices]
        invalid_roles = set(value) - set(roles)
        if invalid_roles:
            raise serializers.ValidationError(f"Invalid role(s). Allowed roles are: {', '.join(roles)}.")
        return value

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please fill password and confirm password.")

        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Confirm password is not equal to password.")

        data.pop('confirm_password', None)
        return data

    def create(self, validated_data):
        roles = validated_data.pop('roles', [])

        user = User.objects.create_user(**validated_data)
        for role in roles:
            user.add_role(role)

        return user

    def update(self, validated_data):
        roles = validated_data.pop('roles', [])

        user = User.objects.create_user(**validated_data)
        for role in roles:
            user.add_role(role)

        return user


class UpdateUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    roles = serializers.ListField(child=serializers.CharField())


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True, validators=[
        contains_number_validator, contains_letter_validator, contains_special_char_validator
    ])
    confirm_password = serializers.CharField()

    def validate_old_password(self, value):
        user = self.context['user']
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Confirm password is not equal to password.")

        try:
            validate_password(data['password'])
        except Exception as e:
            raise serializers.ValidationError("Invalid new password:", e.__str__())

        data.pop('confirm_password', None)
        return data


class PhoneNumberSerializer(BaseModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = '__all__'

    number = serializers.CharField(validators=[phone_number_validator])

    def validate_number(self, number):
        if PhoneNumber.objects.filter(number=number).exists():
            raise serializers.ValidationError("Number already created.")
        return number
