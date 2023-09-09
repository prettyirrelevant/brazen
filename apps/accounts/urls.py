from django.urls import path

from .views import AccountAuthenticationAPIView, AccountCreationAPIView

urlpatterns = [
    path('accounts/create', AccountCreationAPIView.as_view(), name='create-account'),
    path('accounts/authenticate', AccountAuthenticationAPIView.as_view(), name='authenticate-account'),
]
