from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.accounts.choices import State
from common.helpers import error_response, success_response
from services.anchor import AnchorClient

anchor_client = AnchorClient(
    api_key=settings.ANCHOR_API_KEY,
    base_url=settings.ANCHOR_BASE_URL,
)


class VerifyAccountAPIView(APIView):
    permission_classes = (AllowAny,)

    @method_decorator(cache_page(60 * 60 * 24))
    def get(self, request, *args, **kwargs):  # noqa: ARG002
        account_number = kwargs['account_number']
        bank_code_or_id = kwargs['bank_code_or_id']
        resp = anchor_client.verify_account(account_number=account_number, bank_code=bank_code_or_id)
        return success_response(resp['data'])


class AllBanksAPIView(APIView):
    permission_classes = (AllowAny,)

    @method_decorator(cache_page(60 * 60 * 24))
    def get(self, request, *args, **kwargs):  # noqa: ARG002
        all_banks_response = anchor_client.get_banks()
        if all_banks_response is None:
            return error_response(
                message='Error querying all banks from Anchor',
                status_code=status.HTTP_502_BAD_GATEWAY,
            )

        return success_response(all_banks_response['data'])


class AllStatesAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):  # noqa: ARG002
        return success_response(State.values)
