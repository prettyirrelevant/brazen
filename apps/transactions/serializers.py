from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'destination', 'tx_type', 'amount', 'status', 'created_at', 'updated_at')
