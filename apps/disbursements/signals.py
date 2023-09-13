from django.db.models.signals import post_save
from django.dispatch import receiver

from .choices import DisbursementEventStatus
from .models import Disbursement, DisbursementEvent


@receiver(post_save, sender=Disbursement)
def create_initial_disbursement_event(sender, instance, created, **kwargs):  # noqa: ARG001
    if created:
        DisbursementEvent.objects.create(
            disbursement=instance,
            run_at=instance.start_at,
            status=DisbursementEventStatus.NOT_STARTED,
        )
