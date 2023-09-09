from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.beneficiaries.models import Beneficiary
from apps.beneficiaries.serializers import BeneficiarySerializer
from common.helpers import success_response


class BeneficiaryView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BeneficiarySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(data=serializer.data, status_code=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Beneficiary.objects.filter(account=self.request.user)


