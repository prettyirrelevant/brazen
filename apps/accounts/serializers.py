from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from rest_framework import serializers

from .models import Account


class AccountCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, required=True)

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict) from e

        return value

    class Meta:
        model = Account
        fields = (
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'password',
            'address',
            'city',
            'postal_code',
            'country',
            'state',
        )

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)


class AccountAuthenticationSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email

        return token
