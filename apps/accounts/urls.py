from django.urls import path

from .views import (
    AccountAuthenticationAPIView,
    AccountAuthenticationBlacklistAPIView,
    AccountAuthenticationRefreshAPIView,
    AccountCreationAPIView,
    AccountWalletCreationAPIView,
    KYCTierThreeAccountUpgradeAPIView,
    KYCTierTwoAccountUpgradeAPIView,
    MyProfileAPIView,
)

urlpatterns = [
    path('accounts', AccountCreationAPIView.as_view(), name='create-account'),
    path('accounts/authenticate', AccountAuthenticationAPIView.as_view(), name='authenticate-account'),
    path(
        'accounts/jwt/refresh',
        AccountAuthenticationRefreshAPIView.as_view(),
        name='refresh-account-auth-credentials',
    ),
    path(
        'accounts/jwt/blacklist',
        AccountAuthenticationBlacklistAPIView.as_view(),
        name='blacklist-account-auth-credentials',
    ),
    path('accounts/me', MyProfileAPIView.as_view(), name='my-account'),
    path('accounts/wallets', AccountWalletCreationAPIView.as_view(), name='account-wallet-creation'),
    path('accounts/kyc/tier-2', KYCTierTwoAccountUpgradeAPIView.as_view(), name='tier-2-account-upgrade'),
    path('accounts/kyc/tier-3', KYCTierThreeAccountUpgradeAPIView.as_view(), name='tier-3-account-upgrade'),
]
