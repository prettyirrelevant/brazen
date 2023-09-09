from django.db import models

from apps.accounts.models import Account


class TransactionStatus(models.TextChoices):
    FAILED = 'failed'
    PENDING = 'pending'
    REVERSED = 'reversed'
    SUCCESSFUL = 'successful'


class TransactionType(models.TextChoices):
    FUNDING = 'funding'
    DISBURSEMENT = 'disbursement'


class Transaction(models.Model):
    anchor_tx_id = models.CharField('anchor transaction id', max_length=250, unique=True, null=False, blank=False)
    tx_type = models.CharField(
        'transaction type',
        choices=TransactionType.choices,
        max_length=100,
        null=False,
        blank=False,
    )
    source = models.ForeignKey(Account, related_name='transactions', on_delete=models.CASCADE, null=False, blank=False)
    destination = models.CharField('destination', max_length=200, null=False, blank=False)
    amount = models.DecimalField('amount', max_digits=20, decimal_places=2, null=False, blank=False)
    status = models.CharField('status', max_length=50, choices=TransactionStatus.choices, null=False, blank=False)
    retry_count = models.IntegerField('retry count', default=0)
    metadata = models.JSONField('metadata', default=dict)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)
