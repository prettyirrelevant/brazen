from django.db import models


class DisbursementFrequency(models.TextChoices):
    THIRTY_MINS = 'Thirty Minutes'
    HOURLY = 'Hourly'
    WEEKLY = 'Weekly'
    BIWEEKLY = 'Biweekly'
    MONTHLY = 'Monthly'
