from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.accounts.choices import Country, Gender, State
from apps.accounts.managers import AccountManager


class Account(AbstractUser):
    username = None

    email = models.EmailField('email address', unique=True, null=False, blank=False)
    last_name = models.CharField('last name', max_length=150, null=False, blank=False)
    first_name = models.CharField('first name', max_length=150, null=False, blank=False)

    phone_number = models.CharField('phone number', unique=True, max_length=11, null=False, blank=False)

    address = models.TextField('address', null=False, blank=False)
    city = models.CharField('city', max_length=100, null=False, blank=False)
    postal_code = models.IntegerField('postal code', null=False, blank=False)

    gender = models.CharField('gender', max_length=20, choices=Gender.choices)
    country = models.CharField('country', max_length=10, choices=Country.choices, default=Country.NIGERIA)
    state = models.CharField('state', max_length=20, choices=State.choices, null=False, blank=False)

    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    deposit_account_id = models.CharField('deposit account id', max_length=150, null=True, blank=True)
    deposit_account_number = models.CharField('deposit account number', max_length=11, null=True, blank=True)
    deposit_bank_name = models.CharField('deposit bank name', max_length=150, null=True, blank=True)

    customer_id = models.CharField('customer id', max_length=150, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'phone_number')

    objects = AccountManager()
