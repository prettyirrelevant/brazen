from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView, TokenRefreshView

from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from common.helpers import success_response

from .models import Account
from .serializers import AccountCreationSerializer, AccountSerializer


class AccountCreationAPIView(CreateAPIView):
    queryset = Account
    permission_classes = (AllowAny,)
    serializer_class = AccountCreationSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return success_response(data=None, status_code=status.HTTP_201_CREATED)


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
    queryset = Account
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return Account.objects.get(email=self.request.user.email)
