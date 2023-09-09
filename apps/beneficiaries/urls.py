from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.beneficiaries.views import BeneficiaryView


router = DefaultRouter(trailing_slash=True)
router.register("beneficiaries", BeneficiaryView, "beneficiary")

urlpatterns = [
] + router.urls