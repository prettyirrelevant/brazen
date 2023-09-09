from django.db import models

from apps.accounts.models import Account
from apps.beneficiaries.models import Beneficiary
from apps.disbursements.choices import DisbursementFrequency, DisbursementStatus


class Disbursement(models.Model):
    description = models.TextField()
    amount = models.DecimalField(default=0.00, max_digits=12,decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='disbursements')
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='disbursements')
    frequency = models.CharField(max_length=15, choices=DisbursementFrequency.choices, default=DisbursementFrequency.THIRTY_MINS)

    status = models.CharField('status', choices=DisbursementStatus.choices, default=DisbursementStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    next_run_timestamp = models.DateTimeField(null=True, blank=True)

