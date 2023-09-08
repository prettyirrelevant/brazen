from rest_framework import status
from rest_framework.generics import CreateAPIView

from brazen.helpers import success_response

from .models import Account
from .serializers import AccountCreationSerializer


class AccountCreationAPIView(CreateAPIView):
    queryset = Account
    serializer_class = AccountCreationSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return success_response(status_code=status.HTTP_201_CREATED)
