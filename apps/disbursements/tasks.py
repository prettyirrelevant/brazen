from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.disbursements.choices import DisbursementEventStatus, DisbursementStatus
from apps.disbursements.models import MAX_DISBURSEMENT_RETRIES, DisbursementEvent
from apps.transactions.choices import TransactionStatus, TransactionType
from apps.transactions.models import Transaction
from services.anchor import AnchorClient
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.accounts.models import Wallet

anchor_client = AnchorClient(
    api_key=settings.ANCHOR_API_KEY,
    base_url=settings.ANCHOR_BASE_URL,
)


@db_task(retries=MAX_DISBURSEMENT_RETRIES, retry_delay=60)
def initiate_transfer_for_event(event_id):
    with transaction.atomic():
        event = DisbursementEvent.objects.get(id=event_id)
        if event.disbursement_event_transactions.filter(
            status__in=[TransactionStatus.PENDING, TransactionStatus.SUCCESSFUL],
        ).exists():
            return

        event.retries += 1
        transfer_initiation_response = anchor_client.initiate_transfer(
            amount=event.amount,
            reason=event.description,
            account_id=event.account.deposit_account_id,
            counterparty_id=event.beneficiary.counterparty_id,
        )
        if transfer_initiation_response is None:
            raise Exception(f'Something happened while initiating the transfer for event {event.id}')  # noqa: TRY002

        Transaction.objects.create(
            amount=event.amount,
            disbursement_event=event,
            status=TransactionStatus.PENDING,
            source=event.disbursement.account,
            tx_type=TransactionType.DISBURSEMENT,
            destination=event.beneficiary.account_name,
            metadata=transfer_initiation_response['data'],
            anchor_tx_id=transfer_initiation_response['data']['id'],
        )

        event.save()


@db_periodic_task(crontab(minute='*/5'))
def begin_disbursement_events():
    now = timezone.now()
    DisbursementEvent.objects.filter(
        run_at__gte=now,
        retries__lt=MAX_DISBURSEMENT_RETRIES,
        status=DisbursementEventStatus.NOT_STARTED,
        disbursement__status=DisbursementStatus.ACTIVE,
    ).update(status=DisbursementEventStatus.PENDING)


@db_periodic_task(crontab(minute='*/5'))
def initiate_transfers_for_pending_disbursement_events():
    for event in DisbursementEvent.objects.filter(
        retries__lt=MAX_DISBURSEMENT_RETRIES,
        status=DisbursementEventStatus.PENDING,
        disbursement__status=DisbursementStatus.ACTIVE,
    ):
        initiate_transfer_for_event((event.id,), delay=1)


@db_periodic_task(crontab(minute='*/5'))
def disable_disbursements_after_max_retries():
    for event in DisbursementEvent.objects.filter(
        retries=MAX_DISBURSEMENT_RETRIES,
        status=DisbursementEventStatus.PENDING,
        disbursement__status=DisbursementStatus.ACTIVE,
    ):
        # todo: check that all transactions failed.
        event.status = DisbursementEventStatus.FAILURE
        event.disbursement.status = DisbursementStatus.INACTIVE
        event.disbursement.save()
        event.save()
        # todo: send an email that a disbursement has been disabled after several tries.
