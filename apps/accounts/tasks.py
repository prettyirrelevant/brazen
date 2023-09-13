from huey.contrib.djhuey import db_task

from django.conf import settings

from apps.accounts.models import Wallet
from services.anchor import AnchorClient

anchor_client = AnchorClient(
    api_key=settings.ANCHOR_API_KEY,
    base_url=settings.ANCHOR_BASE_URL,
)


@db_task(retries=3)
def fetch_virtual_nuban_info(deposit_account_id: str, wallet_id: int):
    deposit_account_response = anchor_client.get_deposit_account(deposit_account_id)
    if deposit_account_response is None:
        raise Exception(f'Unable to get deposit account info for id {deposit_account_id}')  # noqa: TRY002

    affected_rows = Wallet.objects.filter(id=wallet_id).update(
        bank_name=deposit_account_response['included'][0]['attributes']['bank']['name'],
        account_name=deposit_account_response['included'][0]['attributes']['accountName'],
        account_number=deposit_account_response['included'][0]['attributes']['accountNumber'],
    )
    if affected_rows != 1:
        raise Exception('Unable to set virtual nuban info to wallet')  # noqa: TRY002
