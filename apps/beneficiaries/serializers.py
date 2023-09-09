from rest_framework.serializers import ModelSerializer

from apps.beneficiaries.models import Beneficiary


class BeneficiarySerializer(ModelSerializer):
    class Meta:
        model = Beneficiary
        exclude = ()
        read_only_fields = [
            "account",
            "created_at",
            "updated_at",
        ]
    
    def create(self, validated_data):
        _user = self.context["request"].user
        validated_data["account"] = _user
        beneficiary: Beneficiary = super().create(validated_data)
        return beneficiary