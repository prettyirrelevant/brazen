from rest_framework import serializers

from apps.accounts.serializers import AccountSerializer
from apps.disbursements.serializers import DisbursementEventSerializer

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    disbursement_event = DisbursementEventSerializer()

    class Meta:
        model = Transaction
        fields = (
            'id',
            'account',
            'tx_type',
            'disbursement_event',
            'amount',
            'currency',
            'anchor_ref',
            'status',
            'created_at',
            'updated_at',
        )
