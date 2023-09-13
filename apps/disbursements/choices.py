from django.db import models


class DisbursementFrequency(models.TextChoices):
    THIRTY_MINS = 'Thirty Minutes'
    HOURLY = 'Hourly'
    WEEKLY = 'Weekly'
    BIWEEKLY = 'Biweekly'
    MONTHLY = 'Monthly'


class DisbursementStatus(models.TextChoices):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class DisbursementEventStatus(models.TextChoices):
    FAILURE = 'failure'
    PENDING = 'pending'
    SUCCESS = 'success'
    NOT_STARTED = 'not started'
