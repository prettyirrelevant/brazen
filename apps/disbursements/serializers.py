from decimal import Decimal
from datetime import timedelta
from rest_framework.serializers import ModelSerializer, ValidationError

from apps.disbursements.choices import DisbursementFrequency
from apps.disbursements.models import Disbursement


class DisbursementSerializer(ModelSerializer):
    class Meta:
        model = Disbursement
        exclude = ()
        read_only_fields = [
            'account',
            'created_at',
            'updated_at',
            'status',
            'next_run_timestamp',
        ]

    def create(self, validated_data):
        _user = self.context['request'].user
        validated_data['account'] = _user
        disbursement:Disbursement = super().create(validated_data)

        if disbursement.frequency == DisbursementFrequency.THIRTY_MINS:
            disbursement.next_run_timestamp = disbursement.created_at + timedelta(minutes=30)
        elif disbursement.frequency == DisbursementFrequency.BIWEEKLY:
            disbursement.next_run_timestamp = disbursement.created_at + timedelta(weeks=2)
        elif disbursement.frequency == DisbursementFrequency.HOURLY:
            disbursement.next_run_timestamp = disbursement.created_at + timedelta(hours=1)
        elif disbursement.frequency == DisbursementFrequency.WEEKLY:
            disbursement.next_run_timestamp = disbursement.created_at + timedelta(weeks=1)
        elif disbursement.frequency == DisbursementFrequency.MONTHLY:
            disbursement.next_run_timestamp = disbursement.created_at.replace(day=1) + timedelta(days=32)

        disbursement.save()
        return disbursement

    def validate_amount(self, value):
        _user = self.context['request'].user
        if value > Decimal(_user.balance):
            raise ValidationError(
                'Insufficient Balance', 'insufficient_balance_error',
            )

        return value
