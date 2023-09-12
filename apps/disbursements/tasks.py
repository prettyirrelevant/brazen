from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.accounts.choices import WalletCurrency
from apps.disbursements.choices import DisbursementStatus
from apps.disbursements.models import Disbursement
from apps.transactions.choices import TransactionCategory
from services.anchor import AnchorClient
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.accounts.models import Wallet

anchor_client = AnchorClient(
    api_key=settings.ANCHOR_API_KEY,
    base_url=settings.ANCHOR_BASE_URL,
)


@db_task()
def initiate_disbursement(disbursement_id):
    currency: str = WalletCurrency.NGN

    with transaction.atomic():
        disbursement = Disbursement.objects.get(id=disbursement_id)
        wallet: Wallet = disbursement.account.wallets.filter(currency=currency).first()

        if not wallet:
            # raise error
            return False

        res_json = anchor_client.initiate_transfer(
            amount=disbursement.amount,
            reason=disbursement.description,
            counterparty_id=disbursement.beneficiary.counterparty_id,
            account_id=disbursement.account.deposit_account_id,
        )
        metadata = res_json['data']
        provider_tx_id = res_json['data']['id']

        wallet.pre_debit(
            provider_tx_id=provider_tx_id,
            category=TransactionCategory.DISBURSEMENT,
            amount=disbursement.amount,
            destination=disbursement.beneficiary.account_name,
            metadata=metadata,
        )

        disbursement.update_next_run_timestamp()
        disbursement.save()
        return None


@db_periodic_task(crontab(minute='*/10'))
def check_for_disbursements():
    now = timezone.now()
    all_disbursements = Disbursement.objects.filter(next_run_timestamp__gte=now, status=DisbursementStatus.ACTIVE)
    for disbursement in all_disbursements:
        initiate_disbursement.schedule((disbursement.id,), delay=1)
