from django.db import models


class TransactionStatus(models.TextChoices):
    FAILED = 'failed'
    PENDING = 'pending'
    REVERSED = 'reversed'
    SUCCESSFUL = 'successful'


class TransactionType(models.TextChoices):
    FUNDING = 'funding'
    BILL_PAYMENT = 'bill payment'
    DISBURSEMENT = 'disbursement'
