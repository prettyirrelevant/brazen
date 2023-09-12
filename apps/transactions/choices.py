from django.db import models


class TransactionStatus(models.TextChoices):
    FAILED = 'failed'
    PENDING = 'pending'
    REVERSED = 'reversed'
    SUCCESSFUL = 'successful'


class TransactionType(models.TextChoices):
    CREDIT = 'credit'
    DEBIT = 'debit'


class TransactionCategory(models.TextChoices):
    FUNDING = 'funding'
    DISBURSEMENT = 'disbursement'
    WITHDRAWAL = 'withdrawal'
    REVERSAL = 'reversal'
