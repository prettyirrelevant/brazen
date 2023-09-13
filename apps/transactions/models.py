from django.db import models

from apps.accounts.choices import Currency
from common.models import TimestampedModel

from .choices import TransactionStatus, TransactionType


class Transaction(TimestampedModel):
    tx_type = models.CharField(
        'transaction type',
        choices=TransactionType.choices,
        max_length=100,
        null=False,
        blank=False,
    )
    account = models.ForeignKey(
        'accounts.Account',
        related_name='transactions',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    disbursement_event = models.ForeignKey(
        'disbursements.DisbursementEvent',
        related_name='disbursement_event_transactions',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    metadata = models.JSONField('metadata', default=dict)
    amount = models.DecimalField('amount', max_digits=20, decimal_places=2, null=False, blank=False)
    currency = models.CharField('currency', choices=Currency.choices, max_length=3, null=False, blank=False)
    anchor_ref = models.CharField('anchor reference', max_length=250, unique=True, null=False, blank=False)
    status = models.CharField('status', max_length=50, choices=TransactionStatus.choices, null=False, blank=False)
