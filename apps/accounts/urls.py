from django.urls import path

from .views import (
    AccountAuthenticationAPIView,
    AccountAuthenticationBlacklistAPIView,
    AccountAuthenticationRefreshAPIView,
    AccountCreationAPIView,
    MyProfileAPIView,
    ProfileCreationAPIView,
)

urlpatterns = [
    path('accounts/create', AccountCreationAPIView.as_view(), name='create-account'),
    path('accounts/authenticate', AccountAuthenticationAPIView.as_view(), name='authenticate-account'),
    path(
        'accounts/authenticate/refresh',
        AccountAuthenticationRefreshAPIView.as_view(),
        name='refresh-account-auth-credentials',
    ),
    path(
        'accounts/authenticate/blacklist',
        AccountAuthenticationBlacklistAPIView.as_view(),
        name='blacklist-account-auth-credentials',
    ),
    path('accounts/profile/create', ProfileCreationAPIView.as_view(), name='create-profile'),
    path('accounts/me', MyProfileAPIView.as_view(), name='my-account'),
]
