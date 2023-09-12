from django.conf import settings
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.db import transaction

from rest_framework import serializers

from services.anchor import AnchorClient

from .models import Account, Profile, Wallet

anchor_client = AnchorClient(
    base_url=settings.ANCHOR_BASE_URL,
    api_key=settings.ANCHOR_API_KEY,
)


class AccountCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, required=True)

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages)) from e

        return value

    class Meta:
        model = Account
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
        )



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'gender',
            'phone_number',
            'address',
            'city',
            'postal_code',
            'state',
            'country',
            'date_of_birth',
        )

    # def validate_phone_number(self, value):
    #     if not re.match(r'^(0)([7-9][01])(\d{7})$', value):

    def create(self, validated_data):
        with transaction.atomic():
            _user = self.context['request'].user
            profile: Profile = Profile.objects.create(user=_user, **validated_data)
            resp_json = anchor_client.create_customer(
                first_name=profile.account.first_name,
                last_name=profile.account.last_name,
                email=profile.account.email,
                phone_number=profile.phone_number,
                address=profile.address,
                city=profile.city,
                postal_code=profile.postal_code,
                state=profile.state,
                country=profile.country,
            )
            customer_id = resp_json['data']['id']
            profile.customer_id = customer_id
            profile.save(update_fields=['customer_id'])
        return profile


class WalletSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(max_digits=15, decimal_places=6, read_only=True)
    class Meta:
        model = Wallet
        fields = (
            'balance',
            'currency',
            'account_number',
            'account_name',
            'bank_name',
            'bank_code',
            'is_locked',
            'locked_reason',
        )

        read_only_fields = fields


class AccountSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    wallet = WalletSerializer()
    class Meta:
        model = Account
        fields = '__all__'
