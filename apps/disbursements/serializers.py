from decimal import Decimal

from django.conf import settings

from rest_framework.serializers import ModelSerializer, ValidationError

from apps.accounts.choices import Currency
from apps.disbursements.models import Beneficiary, Disbursement
from services.anchor import AnchorClient

anchor_client = AnchorClient(
    base_url=settings.ANCHOR_BASE_URL,
    api_key=settings.ANCHOR_API_KEY,
)


class BeneficiarySerializer(ModelSerializer):
    class Meta:
        model = Beneficiary
        exclude = ()
        read_only_fields = (
            'account',
            'created_at',
            'updated_at',
            'counterparty_id',
        )

    def create(self, validated_data):
        validated_data['account'] = self.context['request'].user
        beneficiary = super().create(validated_data)

        counterparty_creation_response = anchor_client.create_counterparty(
            account_name=beneficiary.account_name,
            account_number=beneficiary.account_number,
            bank_id=beneficiary.anchor_bank_id,
            bank_code=beneficiary.anchor_bank_code,
        )
        beneficiary.counterparty_id = counterparty_creation_response['data']['id']
        beneficiary.save()
        return beneficiary


class DisbursementSerializer(ModelSerializer):
    class Meta:
        model = Disbursement
        read_only_fields = (
            'account',
            'created_at',
            'updated_at',
            'status',
        )

    def create(self, validated_data):
        validated_data['account'] = self.context['request'].user
        return super().create(validated_data)

    def validate_currency(self, value):
        if value == Currency.DOLLAR:
            raise ValidationError('Dollar disbursements are currently not available.')

        return value

    def validate_amount(self, value):
        if value > Decimal(self.context['request'].user.balance):
            raise ValidationError('Insufficient balance to initiate a disbursement. Kindly top up.')

        return value
