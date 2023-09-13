from decimal import Decimal

from django.conf import settings

from rest_framework.serializers import ModelSerializer, ValidationError

from apps.accounts.choices import Currency
from apps.accounts.serializers import AccountSerializer
from apps.disbursements.models import Beneficiary, Disbursement, DisbursementEvent
from services.anchor import AnchorClient

anchor_client = AnchorClient(
    base_url=settings.ANCHOR_BASE_URL,
    api_key=settings.ANCHOR_API_KEY,
)


class BeneficiarySerializer(ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = (
            'id',
            'tag',
            'account',
            'account_name',
            'anchor_bank_id',
            'account_number',
            'anchor_bank_code',
            'anchor_counterparty_id',
        )
        read_only_fields = (
            'id',
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


class DisbursementEventSerializer(ModelSerializer):
    class Meta:
        model = DisbursementEvent
        fields = ('id', 'retries', 'run_at', 'status')


class DisbursementSerializer(ModelSerializer):
    account = AccountSerializer()
    beneficiary = BeneficiarySerializer()
    events = DisbursementEventSerializer(many=True)

    class Meta:
        model = Disbursement
        fields = (
            'id',
            'amount',
            'status',
            'events',
            'account',
            'start_at',
            'currency',
            'frequency',
            'created_at',
            'updated_at',
            'beneficiary',
            'description',
        )
        read_only_fields = (
            'id',
            'events',
            'status',
            'account',
            'created_at',
            'updated_at',
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
