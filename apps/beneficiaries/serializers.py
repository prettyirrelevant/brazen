from django.conf import settings

from rest_framework.serializers import ModelSerializer

from apps.beneficiaries.models import Beneficiary
from services.anchor import AnchorClient

anchor_client = AnchorClient(
    base_url=settings.ANCHOR_BASE_URL,
    api_key=settings.ANCHOR_API_KEY,
)


class BeneficiarySerializer(ModelSerializer):
    class Meta:
        model = Beneficiary
        exclude = ()
        read_only_fields = [
            'account',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        _user = self.context['request'].user
        validated_data['account'] = _user
        beneficiary: Beneficiary = super().create(validated_data)
        resp_json = anchor_client.create_counterparty(
            account_name=beneficiary.account_name,
            account_number=beneficiary.account_number,
            bank_id=beneficiary.bank_id,
            bank_code=beneficiary.bank_code,
        )
        counterparty_id = resp_json['data']['id']
        beneficiary.counterparty_id = counterparty_id
        beneficiary.save()
        return beneficiary
