from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.accounts.choices import Country, State
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

    country = models.CharField('country', max_length=10, choices=Country.choices, default=Country.NIGERIA)
    state = models.CharField('state', max_length=20, choices=State.choices, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'phone_number')

    objects = AccountManager()
