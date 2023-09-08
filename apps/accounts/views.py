from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from brazen.helpers import success_response

from .models import Account
from .serializers import AccountAuthenticationSerializer, AccountCreationSerializer


class AccountCreationAPIView(CreateAPIView):
    queryset = Account
    permission_classes = (AllowAny,)
    serializer_class = AccountCreationSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return success_response(data=None, status_code=status.HTTP_201_CREATED)


class AccountAuthenticationAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = AccountAuthenticationSerializer
