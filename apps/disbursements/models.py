import calendar
from typing import ClassVar

from dateutil.relativedelta import relativedelta

from django.db import models

from apps.accounts.choices import Currency
from common.models import TimestampedModel

from .choices import DisbursementEventStatus, DisbursementFrequency, DisbursementStatus

MAX_DISBURSEMENT_RETRIES = 3


class Beneficiary(TimestampedModel, models.Model):
    account = models.ForeignKey(
        'accounts.Account',
        on_delete=models.SET_NULL,
        related_name='beneficiaries',
        null=True,
        blank=True,
    )
    tag = models.CharField('tag', max_length=150, null=True, blank=True)

    account_number = models.CharField(max_length=11, null=False, blank=False)
    account_name = models.CharField(max_length=150, null=False, blank=False)

    anchor_bank_code = models.CharField(max_length=150, null=False, blank=False)
    anchor_bank_id = models.CharField(max_length=150, null=False, blank=False)
    anchor_counterparty_id = models.CharField(max_length=150, null=False, blank=False)

    class Meta:
        constraints: ClassVar[list] = [
            models.UniqueConstraint(
                fields=('account', 'account_number'),
                name='account_and_account_number_unique',
            ),
        ]


class Disbursement(TimestampedModel):
    description = models.TextField(null=True, blank=True)
    start_at = models.DateTimeField('start at', null=False, blank=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False)
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='disbursements')
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name='disbursements')
    currency = models.CharField('currency', choices=Currency.choices, max_length=3, null=False, blank=False)
    frequency = models.CharField(
        max_length=15,
        choices=DisbursementFrequency.choices,
        default=DisbursementFrequency.THIRTY_MINS,
    )
    status = models.CharField(
        'status',
        choices=DisbursementStatus.choices,
        default=DisbursementStatus.ACTIVE,
        max_length=20,
    )


class DisbursementEvent(TimestampedModel):
    retries = models.IntegerField('retries', default=0)
    run_at = models.DateTimeField('run at', null=False, blank=False)
    disbursement = models.ForeignKey(Disbursement, on_delete=models.CASCADE, related_name='events')
    status = models.CharField(
        'status',
        max_length=20,
        choices=DisbursementEventStatus.choices,
        null=False,
        blank=False,
    )

    def create_next_disbursement_event(self) -> None:
        if self.disbursement.frequency == DisbursementFrequency.THIRTY_MINS:
            run_at = self.run_at + relativedelta(minutes=30)
        if self.disbursement.frequency == DisbursementFrequency.BIWEEKLY:
            run_at = self.run_at + relativedelta(weeks=2)
        if self.disbursement.frequency == DisbursementFrequency.HOURLY:
            run_at = self.run_at + relativedelta(hours=1)
        if self.disbursement.frequency == DisbursementFrequency.WEEKLY:
            run_at = self.run_at + relativedelta(weeks=1)
        if self.disbursement.frequency == DisbursementFrequency.MONTHLY:
            run_at = self.run_at + relativedelta(months=1)
            if run_at.day < self.disbursement.start_at.day:
                max_day = calendar.monthrange(run_at.year, run_at.month)[1]
                if self.disbursement.start_at.day <= max_day:
                    run_at = run_at.replace(day=self.disbursement.start_at.day)

        DisbursementEvent.objects.create(
            run_at=run_at,
            disbursement=self.disbursement,
            status=DisbursementEventStatus.NOT_STARTED,
        )
