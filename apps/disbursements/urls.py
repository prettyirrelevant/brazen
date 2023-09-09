from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.disbursements.views import DisbursementView


router = DefaultRouter(trailing_slash=True)
router.register("disbursements", DisbursementView, "disbursement")

urlpatterns = [
] + router.urls