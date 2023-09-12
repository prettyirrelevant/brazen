from django.db import models

from common.models import BaseModel

from .choices import TransactionCategory, TransactionStatus, TransactionType


class Transaction(BaseModel):
    provider_tx_id = models.CharField('provider transaction id', max_length=250, unique=True, null=False, blank=False)
    tx_type = models.CharField(
        'transaction type',
        choices=TransactionType.choices,
        max_length=100,
        null=False,
        blank=False,
    )
    category = models.CharField(
        'transaction type',
        choices=TransactionCategory.choices,
        max_length=100,
        null=False,
        blank=False,
    )
    account = models.ForeignKey('accounts.Account', related_name='transactions', on_delete=models.CASCADE, null=True, blank=True)
    wallet = models.ForeignKey('accounts.Wallet', related_name='transactions', on_delete=models.CASCADE, null=False, blank=False)

    destination = models.CharField('destination', max_length=200, null=False, blank=False)

    amount = models.DecimalField('amount', max_digits=20, decimal_places=2, null=False, blank=False)
    previous_balance = models.DecimalField('previous balance', max_digits=20, decimal_places=2, null=True, blank=True)

    status = models.CharField('status', max_length=50, choices=TransactionStatus.choices, null=False, blank=False)
    retry_count = models.IntegerField('retry count', default=0)
    is_reversal = models.BooleanField(default=False)
    metadata = models.JSONField('metadata', default=dict)

