from django.urls import path

from .views import AccountCreationAPIView

urlpatterns = [
    path('accounts/create', AccountCreationAPIView.as_view(), name='create-account'),
]
