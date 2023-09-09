from django.db import models

from apps.accounts.models import Account


class Beneficiary(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='beneficiaries', null=True, blank=True)
    name = models.CharField('name', max_length=150, null=True, blank=True)
    account_number = models.CharField(max_length=11, unique=True, null=False, blank=False)
    account_name = models.CharField(max_length=150, null=True, blank=False)
    bank_code = models.CharField(max_length=150, null=True, blank=False)
    bank_id = models.CharField(max_length=150, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

