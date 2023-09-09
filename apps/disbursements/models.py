from datetime import timedelta

from django.db import models

from apps.accounts.models import Account
from apps.beneficiaries.models import Beneficiary
from apps.disbursements.choices import DisbursementFrequency, DisbursementStatus


class Disbursement(models.Model):
    description = models.TextField()
    amount = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='disbursements')
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='disbursements')
    frequency = models.CharField(
        max_length=15,
        choices=DisbursementFrequency.choices,
        default=DisbursementFrequency.THIRTY_MINS,
    )

    status = models.CharField('status', max_length=100, choices=DisbursementStatus.choices, default=DisbursementStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    next_run_timestamp = models.DateTimeField(null=True, blank=True)

    def update_next_run_timestamp(self):
        if self.frequency == DisbursementFrequency.THIRTY_MINS:
            self.next_run_timestamp = self.next_run_timestamp + timedelta(minutes=30)
        elif self.frequency == DisbursementFrequency.BIWEEKLY:
            self.next_run_timestamp = self.next_run_timestamp + timedelta(weeks=2)
        elif self.frequency == DisbursementFrequency.HOURLY:
            self.next_run_timestamp = self.next_run_timestamp + timedelta(hours=1)
        elif self.frequency == DisbursementFrequency.WEEKLY:
            self.next_run_timestamp = self.next_run_timestamp + timedelta(weeks=1)
        elif self.frequency == DisbursementFrequency.MONTHLY:
            self.next_run_timestamp = self.next_run_timestamp.replace(day=1) + timedelta(days=32)
