import re

from django.conf import settings
from django.db import transaction

from rest_framework import serializers

from services.anchor import AnchorClient

from .choices import KYC, Currency, Gender, KYCTierThreeDocumentType, State
from .models import Account, Profile, Wallet
from .tasks import fetch_virtual_nuban_info

anchor_client = AnchorClient(
    api_key=settings.ANCHOR_API_KEY,
    base_url=settings.ANCHOR_BASE_URL,
)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'email',
            'first_name',
            'last_name',
            'date_joined',
        )


class AccountCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, required=True, write_only=True)

    class Meta:
        model = Account
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
        )

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)


class KYCTierTwoUpgradeSerializer(serializers.ModelSerializer):
    bvn = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    postal_code = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)
    state = serializers.ChoiceField(required=True, choices=State.choices)
    gender = serializers.ChoiceField(required=True, choices=Gender.choices)

    class Meta:
        model = Profile
        fields = (
            'address',
            'gender',
            'postal_code',
            'city',
            'state',
            'phone_number',
            'date_of_birth',
            'bvn',
            'gender',
        )

    def validate_phone_number(self, value):
        # https://regexr.com/7k0fm
        if not re.match(r'^(0[789])([01]\d{8})$', value):
            raise serializers.ValidationError('Invalid phone number provided.')

        return value

    def validate(self, attrs):
        if self.context['request'].user.profile.kyc_level != KYC.TIER_1:
            raise serializers.ValidationError('You have already upgraded to Tier 2.')

        return super().validate(attrs)

    def update(self, instance, validated_data):
        with transaction.atomic():
            profile = super().update(instance, validated_data)
            customer_creation_response = anchor_client.create_customer(
                city=profile.city,
                address=profile.address,
                state=profile.state,
                email=profile.account.email,
                postal_code=profile.postal_code,
                phone_number=profile.phone_number,
                last_name=profile.account.last_name,
                first_name=profile.account.first_name,
            )
            if customer_creation_response is None:
                raise serializers.ValidationError('Unable to create customer account on Anchor.')

            tier_two_kyc_verification_response = anchor_client.kyc_tier_two_verification(
                bvn=profile.bvn,
                dob=profile.date_of_birth.isoformat(),
                gender=profile.gender,
                customer_id=customer_creation_response['data']['id'],
            )
            if tier_two_kyc_verification_response is None:
                anchor_client.delete_customer(customer_creation_response['data']['id'])
                raise serializers.ValidationError('Unable to perform KYC Tier 2 verification.')

            profile.kyc_level = KYC.TIER_2
            profile.anchor_customer_id = customer_creation_response['data']['id']

            profile.save(update_fields=['kyc_level', 'anchor_customer_id'])
            return profile


class KYCTierThreeUpgradeSerializer(serializers.ModelSerializer):
    document_identifier = serializers.CharField(required=True)
    document_expiry_date = serializers.DateField(required=True)
    document_type = serializers.ChoiceField(required=True, choices=KYCTierThreeDocumentType.choices)

    class Meta:
        model = Profile
        fields = ('document_identifier', 'document_expiry_date', 'document_type')

    def validate(self, attrs):
        if self.context['request'].user.profile.kyc_level == KYC.TIER_1:
            raise serializers.ValidationError('You have to upgrade to Tier 2 first.')

        if self.context['request'].user.profile.kyc_level == KYC.TIER_3:
            raise serializers.ValidationError('You have already upgraded to Tier 3.')

        return super().validate(attrs)

    def update(self, instance, validated_data):
        with transaction.atomic():
            profile = super().update(instance, validated_data)
            tier_three_kyc_verification_response = anchor_client.kyc_tier_three_verification(
                id_type=profile.document_type,
                id_number=profile.document_identifier,
                customer_id=profile.anchor_customer_id,
                id_expiry_date=profile.document_expiry_date.isoformat(),
            )
            if tier_three_kyc_verification_response is None:
                raise serializers.ValidationError('Unable to perform KYC Tier 3 verification.')

            profile.kyc_level = KYC.TIER_3
            profile.save(update_fields=['kyc_level'])
            return profile


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = (
            'currency',
            'balance',
            'bank_name',
            'account_name',
            'account_number',
            'anchor_deposit_account_id',
            'is_locked',
            'is_locked_reason',
        )

        read_only_fields = (
            'balance',
            'bank_name',
            'account_name',
            'account_number',
            'anchor_deposit_account_id',
            'is_locked',
            'is_locked_reason',
        )

    def validate(self, attrs):
        if self.context['request'].user.profile.kyc_level == KYC.TIER_1:
            raise serializers.ValidationError('Please upgrade your account to at least Tier 2 to create a wallet.')

        if attrs['currency'] == Currency.DOLLAR:
            raise serializers.ValidationError('Dollar accounts are currently not available.')

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        with transaction.atomic():
            validated_data['account'] = user
            wallet = super().create(validated_data)
            deposit_account_creation_response = anchor_client.create_deposit_account(user.profile.anchor_customer_id)
            if deposit_account_creation_response is None:
                raise serializers.ValidationError('Unable to create deposit account on Anchor.')

            wallet.anchor_deposit_account_id = deposit_account_creation_response['data']['id']
            wallet.save()

            fetch_virtual_nuban_info.schedule((deposit_account_creation_response['data']['id'], wallet.id), delay=2)
            return wallet


class ProfileSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    wallets = WalletSerializer(many=True, source='account.wallets')

    class Meta:
        model = Profile
        fields = ('account', 'gender', 'state', 'country', 'kyc_level', 'wallets')
