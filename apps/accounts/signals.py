from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Account, Profile


@receiver(post_save, sender=Account)
def create_profile(sender, instance, created, **kwargs):  # noqa: ARG001
    if created:
        Profile.objects.create(account=instance)
