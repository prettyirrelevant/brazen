from decimal import Decimal

from rest_framework.serializers import ModelSerializer, ValidationError

from apps.disbursements.models import Disbursement


class DisbursementSerializer(ModelSerializer):
    class Meta:
        model = Disbursement
        exclude = ()
        read_only_fields = [
            'account',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        _user = self.context['request'].user
        validated_data['account'] = _user
        disbursement:Disbursement = super().create(validated_data)
        return disbursement

    def validate_amount(self, value):
        _user = self.context['request'].user
        if value > Decimal(_user.balance):
            raise ValidationError(
                'Insufficient Balance', 'insufficient_balance_error',
            )

        return value
