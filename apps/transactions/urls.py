from django.urls import path

from .views import TransactionsAPIView, WebhookAPIView

urlpatterns = [
    path('transactions', TransactionsAPIView.as_view(), name='get-transactions'),
    path('webhook', WebhookAPIView.as_view(), name='webhook'),
]
