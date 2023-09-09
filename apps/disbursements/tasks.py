from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.disbursements.choices import DisbursementStatus
from apps.disbursements.models import Disbursement
from apps.transactions.models import Transaction, TransactionStatus
from services.anchor import AnchorClient

anchor_client = AnchorClient(
    api_key=settings.ANCHOR_API_KEY,
    base_url=settings.ANCHOR_BASE_URL,
)


@db_task()
def initiate_disbursement(disbursement_id):
    with transaction.atomic():
        disbursement = Disbursement.objects.get(id=disbursement_id)
        res_json = anchor_client.initiate_transfer(
            amount=disbursement.amount,
            reason=disbursement.description,
            counterparty_id=disbursement.beneficiary.counterparty_id,
            account_id=disbursement.account.deposit_account_id,
        )
        Transaction.objects.create(
            anchor_tx_id=res_json['data']['id'],
            metadata=res_json['data'],
            amount=disbursement.amount,
            source=disbursement.account,
            status=TransactionStatus.PENDING,
            destination=disbursement.beneficiary.account_name,
        )

        disbursement.update_next_run_timestamp()
        disbursement.save()


@db_periodic_task(crontab(minute='*/10'))
def check_for_disbursements():
    now = timezone.now()
    all_disbursements = Disbursement.objects.filter(next_run_timestamp__gte=now, status=DisbursementStatus.ACTIVE)
    for disbursement in all_disbursements:
        initiate_disbursement.schedule((disbursement.id,), delay=1)
