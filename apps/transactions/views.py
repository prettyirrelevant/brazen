import logging
from decimal import Decimal

from django.conf import settings
from django.db import transaction

from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.accounts.choices import Currency
from apps.accounts.models import Wallet
from common.helpers import success_response
from services.anchor import AnchorClient

from .choices import TransactionStatus
from .models import Transaction
from .serializers import TransactionSerializer

anchor_client = AnchorClient(
    api_key=settings.ANCHOR_API_KEY,
    base_url=settings.ANCHOR_BASE_URL,
)


logger = logging.getLogger(__name__)


class WebhookAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):  # noqa: ARG002
        logger.info(f'Webhook payload is: {request.data}')

        if request.data['data']['type'] == 'payment.settled':
            metadata = request.data['data']['attributes']['payment']
            wallet = Wallet.objects.get(
                anchor_deposit_account_id=metadata['settlementAccount']['accountId'],
            )
            wallet.credit(
                metadata=metadata,
                provider_ref=metadata['paymentId'],
                currency=Currency(metadata['currency']),
                amount_in_least_denomination=Decimal(metadata['amount']),
            )

        if request.data['data']['type'] == 'nip.transfer.successful':
            metadata = request.data['data']
            with transaction.atomic():
                tx = Transaction.objects.get(anchor_ref=metadata['relationships']['transfer']['data']['id'])
                wallet = tx.account.wallets.get(
                    anchor_deposit_account_id=metadata['relationships']['account']['data']['id'],
                )
                wallet.debit(tx=tx, metadata=metadata)
                tx.disbursement_event.create_next_disbursement_event()

        if request.data['data']['type'] == 'nip.transfer.failed':
            tx = Transaction.objects.get(anchor_tx_id=request.data['data']['relationships']['transfer']['data']['id'])
            tx.metadata = request.data['data']
            tx.status = TransactionStatus.FAILED
            tx.save()

        if request.data['data']['type'] == 'nip.transfer.reversed':
            tx = Transaction.objects.get(anchor_tx_id=request.data['data']['relationships']['transfer']['data']['id'])
            tx.metadata = request.data['data']
            tx.status = TransactionStatus.REVERSED
            tx.save()

        return success_response(data=None)


class TransactionsAPIView(ListAPIView):
    queryset = Transaction.objects.get_queryset()
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(source=self.request.user)

    def list(self, request, *args, **kwargs):  # noqa: A003
        response = super().list(request, *args, **kwargs)
        return success_response(response.data)


class VerifyAccountAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):  # noqa: ARG002
        account_number = kwargs['account_number']
        bank_code_or_id = kwargs['bank_code_or_id']
        resp = anchor_client.verify_account(account_number=account_number, bank_code=bank_code_or_id)
        return resp['data']
