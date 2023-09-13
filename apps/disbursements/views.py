from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from common.helpers import success_response

from .models import Beneficiary, Disbursement
from .serializers import BeneficiarySerializer, DisbursementSerializer


class BeneficiaryView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = BeneficiarySerializer
    queryset = Beneficiary.objects.get_queryset()

    def create(self, request, *args, **kwargs):  # noqa: ARG002
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(data=serializer.data, status_code=status.HTTP_201_CREATED)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(account=self.request.user)


class DisbursementView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = DisbursementSerializer
    queryset = Disbursement.objects.get_queryset()

    def create(self, request, *args, **kwargs):  # noqa: ARG002
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(data=serializer.data, status_code=status.HTTP_201_CREATED)

    def get_queryset(self):
        qs = super().get_queryset()
        if getattr(self, 'swagger_fake_view', False):
            return qs

        return qs.filter(account=self.request.user)
