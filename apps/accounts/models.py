import uuid
from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from apps.accounts.choices import Country, Gender, State, WalletCurrency
from apps.accounts.managers import AccountManager
from apps.transactions.models import Transaction, TransactionType, TransactionStatus
from common.models import BaseModel

class Account(AbstractUser):
    username = None

    uid = models.UUIDField(unique=True, editable=False, null=False, default=uuid.uuid4)
    email = models.EmailField('email address', unique=True, null=False, blank=False)
    last_name = models.CharField('last name', max_length=150, null=False, blank=False)
    first_name = models.CharField('first name', max_length=150, null=False, blank=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name')

    objects = AccountManager()


class Profile(BaseModel):
    account = models.OneToOneField(
        Account,
        on_delete=models.SET_NULL,
        related_name='profile',
        null=True,
        blank=True,
    )
    phone_number = models.CharField('phone number', unique=True, max_length=11, null=False, blank=False)

    address = models.TextField('address', null=False, blank=False)
    city = models.CharField('city', max_length=100, null=False, blank=False)
    postal_code = models.IntegerField('postal code', null=False, blank=False)

    gender = models.CharField('gender', max_length=20, choices=Gender.choices)
    country = models.CharField('country', max_length=10, choices=Country.choices, default=Country.NIGERIA)
    state = models.CharField('state', max_length=20, choices=State.choices, null=False, blank=False)

    date_of_birth = models.DateField('date of birth')
    # TODO: encrypt bvn data
    bvn =  models.CharField(
        "Bank Verification Number", max_length=128, blank=True, null=True, editable=False
    )
    
    customer_id = models.CharField('customer id', max_length=150, null=True, blank=True)
    

class Wallet(BaseModel):
    account = models.OneToOneField(
        Account,
        on_delete=models.SET_NULL,
        related_name='wallet',
        null=True,
        blank=True,
    )
    profile = models.OneToOneField(
        Profile,
        on_delete=models.SET_NULL,
        related_name='wallet',
        null=True,
        blank=True,
    )
    currency = models.CharField(
        'currency', 
        max_length=10, 
        choices=WalletCurrency.choices, 
        default=WalletCurrency.NAIRA
    )

    provider_account_id = models.CharField('provider account id', max_length=150, null=False, blank=False)
    account_number = models.CharField('deposit account number', max_length=11, null=False, blank=False)
    account_name =  models.CharField('deposit account name', max_length=150, null=False, blank=False)
    bank_name = models.CharField('deposit bank name', max_length=150, null=False, blank=False)
    bank_code = models.CharField('deposit bank code', max_length=150, null=False, blank=False)

    _balance = models.DecimalField(
        max_digits=15, 
        decimal_places=6, 
        default=0.00,
        db_column="balance",
        editable=False,
    )

    is_locked = models.BooleanField(default=False)
    locked_reason = models.CharField(max_length=1024, blank=True, default="")

    class Meta:
        unique_together = ("account", "profile", "currency")

    @property
    def balance(self) -> Decimal:
        return self._balance

    def create_transaction_record(self) -> Transaction:
        pass

    def credit(
        self,
        amount: Decimal,
        narration: str,
        reference: str,
        **kwargs,
    ) -> Transaction:
        transaction_type: str = TransactionType.FUNDING

        with transaction.atomic():
            __balance = self._balance
            transaction = self.create_transaction_record()

        return transaction

    def debit(
        self,
        amount: Decimal,
        narration: str,
        reference: str,
        **kwargs,
    ) -> Transaction:
        transaction_type: str = TransactionType.DISBURSEMENT

        if self.is_locked:
            raise ValidationError(
                "Wallet is locked",
                code="wallet_locked",
            )

        with transaction.atomic():
            __balance = self._balance
            transaction = self.create_transaction_record()

        return transaction



