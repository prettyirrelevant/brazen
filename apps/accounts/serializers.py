
from django.conf import settings
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.db import transaction

from rest_framework import serializers

from services.anchor import AnchorClient

from .models import Account

anchor_client = AnchorClient(
    base_url=settings.ANCHOR_BASE_URL,
    api_key=settings.ANCHOR_API_KEY,
)


class AccountCreationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, required=True)

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages)) from e

        return value

    # def validate_phone_number(self, value):
    #     if not re.match(r'^(0)([7-9][01])(\d{7})$', value):

    class Meta:
        model = Account
        fields = (
            'email',
            'first_name',
            'last_name',
            'gender',
            'phone_number',
            'password',
            'address',
            'city',
            'postal_code',
            'country',
            'state',
        )
        read_only_fields = [
            "country",
        ]

    def create(self, validated_data):
        with transaction.atomic():
            account: Account = Account.objects.create_user(**validated_data)
            resp_json = anchor_client.create_customer(
                first_name=account.first_name,
                last_name=account.last_name,
                email=account.email,
                phone_number=account.phone_number,
                address=account.address,
                city=account.city,
                postal_code=account.postal_code,
                state=account.state,
            )
            customer_id = resp_json['data']['id']
            anchor_client.verify_kyc(customer_id=customer_id, gender=account.gender)
            resp_json = anchor_client.create_deposit_account(
                customer_id=customer_id,
            )

            deposit_account_id = resp_json['data']['id']
            deposit_account_number = resp_json['data']['attributes']['accountNumber']
            deposit_bank_name = resp_json['data']['attributes']['bank']['name']

            account.customer_id = customer_id
            account.deposit_account_id = deposit_account_id
            account.deposit_account_number = deposit_account_number
            account.deposit_bank_name = deposit_bank_name
            account.save(update_fields=[
                'customer_id',
                'deposit_account_id',
                'deposit_account_number',
                'deposit_bank_name',
            ])

        return account
