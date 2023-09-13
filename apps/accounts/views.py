from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView, TokenRefreshView

from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated

from common.helpers import success_response

from .models import Account, Profile
from .serializers import (
    AccountCreationSerializer,
    KYCTierThreeUpgradeSerializer,
    KYCTierTwoUpgradeSerializer,
    ProfileSerializer,
    WalletSerializer,
)


class AccountCreationAPIView(CreateAPIView):
    queryset = Account.objects.get_queryset()
    permission_classes = (AllowAny,)
    serializer_class = AccountCreationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return success_response(data=response.data, status_code=status.HTTP_201_CREATED)


class KYCTierTwoAccountUpgradeAPIView(UpdateModelMixin, GenericAPIView):
    queryset = Profile.objects.get_queryset()
    permission_classes = (IsAuthenticated,)
    serializer_class = KYCTierTwoUpgradeSerializer

    def get_object(self):
        qs = self.get_queryset()
        return qs.get(account=self.request.user)

    def post(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return success_response(response.data)


class KYCTierThreeAccountUpgradeAPIView(UpdateModelMixin, GenericAPIView):
    queryset = Profile.objects.get_queryset()
    permission_classes = (IsAuthenticated,)
    serializer_class = KYCTierThreeUpgradeSerializer

    def get_object(self):
        qs = self.get_queryset()
        return qs.get(account=self.request.user)

    def post(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return success_response(response.data)


class AccountWalletCreationAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WalletSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return success_response(response.data)


class AccountAuthenticationAPIView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return success_response(response.data)


class AccountAuthenticationRefreshAPIView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return success_response(data=response.data, status_code=response.status_code)


class AccountAuthenticationBlacklistAPIView(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return success_response(data=response.data, status_code=response.status_code)


class MyProfileAPIView(RetrieveAPIView):
    queryset = Profile.objects.prefetch_related('account__wallets')
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.get_queryset().get(account__email=self.request.user.email)
