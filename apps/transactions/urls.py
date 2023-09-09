from django.urls import path

from .views import TransactionsAPIView, VerifyAccountAPIView, WebhookAPIView

urlpatterns = [
    path('transactions', TransactionsAPIView.as_view(), name='get-transactions'),
    path('verify-account', VerifyAccountAPIView.as_view(), name='verify-account'),
    path('webhook', WebhookAPIView.as_view(), name='webhook'),
]
