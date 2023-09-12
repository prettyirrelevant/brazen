import logging
from decimal import Decimal

from django.conf import settings
from django.db import transaction

from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.accounts.models import Wallet
from common.helpers import success_response
from services.anchor import AnchorClient

from .choices import TransactionCategory, TransactionStatus
from .models import Transaction
from .serializers import TransactionSerializer

anchor_client = AnchorClient(
    api_key=settings.ANCHOR_API_KEY,
    base_url=settings.ANCHOR_BASE_URL,
)


logger = logging.getLogger(__name__)


class WebhookAPIView(APIView):
    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request, *args, **kwargs):  # noqa: ARG002
        logger.info(f'Webhook payload is: {request.data}')
        if request.data['data']['type'] == 'payment.settled':
            account_id: str = request.data['data']['attributes']['payment']['settlementAccount']['accountId']
            currency: str = request.data['data']['attributes']['payment']['currency']
            amount_in_kobo: float = request.data['data']['attributes']['payment']['amount']
            provider_tx_id: str = request.data['data']['attributes']['payment']['paymentId']

            amount_in_ngn = Decimal(amount_in_kobo / 100)
            wallet: Wallet = Wallet.objects.get(provider_account_id=account_id, currency=currency.upper())

            wallet.credit(
                provider_tx_id=provider_tx_id,
                amount = amount_in_ngn,
                category=TransactionCategory.FUNDING,
                metadata=request.data,
            )

        if request.data['data']['type'] == 'nip.transfer.successful':
            tx = Transaction.objects.get(anchor_tx_id=request.data['data']['relationships']['transfer']['data']['id'])
            with transaction.atomic:
                tx.metadata = request.data
                tx.status = TransactionStatus.SUCCESSFUL
                tx.wallet.credit(transaction=tx)
                tx.save()

        if request.data['data']['type'] == 'nip.transfer.failed':
            tx = Transaction.objects.get(anchor_tx_id=request.data['data']['relationships']['transfer']['data']['id'])
            tx.metadata = request.data
            tx.status = TransactionStatus.FAILED
            tx.save()

        return success_response(data=None)


class TransactionsAPIView(ListAPIView):
    queryset = Transaction.objects.get_queryset()
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return []
        qs = super().get_queryset()
        return qs.filter(source=self.request.user)

    def list(self, request, *args, **kwargs):  # noqa: A003
        response = super().list(request, *args, **kwargs)
        return success_response(response.data)


class VerifyAccountAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        account_number = kwargs['account_number']
        bank_code_or_id = kwargs['bank_code_or_id']
        resp = anchor_client.verify_account(account_number=account_number, bank_code=bank_code_or_id)
        return resp['data']
