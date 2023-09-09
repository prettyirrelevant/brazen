from apps.disbursements.choices import DisbursementFrequency
from apps.disbursements.models import Disbursement

def update_next_run_timestamp(disbursement):
    if disbursement.frequency == DisbursementFrequency.THIRTY_MINS:
        disbursement.next_run_timestamp = disbursement.created_at + timedelta(minutes=30)
    elif disbursement.frequency == DisbursementFrequency.BIWEEKLY:
        disbursement.next_run_timestamp = disbursement.created_at + timedelta(weeks=2)
    elif disbursement.frequency == DisbursementFrequency.HOURLY:
        disbursement.next_run_timestamp = disbursement.created_at + timedelta(hours=1)
    elif disbursement.frequency == DisbursementFrequency.WEEKLY:
        disbursement.next_run_timestamp = disbursement.created_at + timedelta(weeks=1)
    elif disbursement.frequency == DisbursementFrequency.MONTHLY:
        disbursement.next_run_timestamp = disbursement.created_at.replace(day=1) + timedelta(days=32)