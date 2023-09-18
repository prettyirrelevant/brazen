from rest_framework.routers import DefaultRouter

from apps.disbursements.views import BeneficiaryView, DisbursementView

router = DefaultRouter(trailing_slash=False)
router.register('beneficiaries', BeneficiaryView, 'beneficiary')
router.register('disbursements', DisbursementView, 'disbursement')


urlpatterns = [*router.urls]
