
from rest_framework.routers import DefaultRouter

from apps.disbursements.views import DisbursementView

router = DefaultRouter(trailing_slash=False)
router.register('disbursements', DisbursementView, 'disbursement')

urlpatterns = [*router.urls]
