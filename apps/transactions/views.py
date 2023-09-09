from django.conf import settings
from django.db import transaction
import logging

from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.accounts.models import Account
from common.helpers import success_response
from services.anchor import AnchorClient

from .models import Transaction, TransactionStatus, TransactionType
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
            source = Account.objects.get(
                deposit_account_id=request.data['data']['attributes']['payment']['settlementAccount']['accountId'],
            )
            Transaction.objects.create(
                anchor_tx_id=request.data['data']['attributes']['payment']['paymentId'],
                source=source,
                destination='self',
                tx_type=TransactionType.FUNDING,
                amount=request.data['data']['attributes']['payment']['amount'] / 100,
                status=TransactionStatus.SUCCESSFUL,
                metadata=request.data,
            )

            # NOTE: This should not be like this i.e. race condition
            source.balance += request.data['attributes']['payment']['amount'] / 100
            source.save()

        if request.data['data']['type'] == 'nip.transfer.successful':
            tx = Transaction.objects.get(anchor_tx_id=request.data['data']['relationships']['transfer']['data']['id'])
            tx.metadata = request.data
            tx.status = TransactionStatus.SUCCESSFUL

            # NOTE: This should not be like this i.e. race condition
            tx.source.balance -= tx.amount
            tx.source.save()
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
