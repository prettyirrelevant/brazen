from django.urls import path

from .views import AllBanksAPIView, AllStatesAPIView, VerifyAccountAPIView

urlpatterns = [
    path('core/banks', AllBanksAPIView.as_view(), name='all-banks'),
    path('core/states', AllStatesAPIView.as_view(), name='all-states'),
    path(
        'core/verify-bank-account/<account_number>/<bank_code_or_id>',
        VerifyAccountAPIView.as_view(),
        name='verify-bank-account',
    ),
]
