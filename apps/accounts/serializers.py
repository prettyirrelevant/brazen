import re

from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from rest_framework import serializers

from .models import Account


class AccountCreationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, required=True)

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages)) from e

        return value

    def validate_phone_number(self, value):
        if not re.match(r'^(0)([7-9][01])(\d{7})$', value):
            raise serializers.ValidationError('Phone number provided is not a valid Nigerian number.')

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
