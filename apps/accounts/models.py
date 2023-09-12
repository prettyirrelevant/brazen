import uuid
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from apps.accounts.choices import Country, Gender, State, WalletCurrency
from apps.accounts.managers import AccountManager
from apps.transactions.models import Transaction, TransactionStatus, TransactionType
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
        'Bank Verification Number', max_length=128, blank=True, null=True, editable=False,
    )

    customer_id = models.CharField('customer id', max_length=150, null=True, blank=True)


class Wallet(BaseModel):
    account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        related_name='wallets',
        null=True,
        blank=True,
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        related_name='wallets',
        null=True,
        blank=True,
    )
    currency = models.CharField(
        'currency',
        max_length=10,
        choices=WalletCurrency.choices,
        default=WalletCurrency.NAIRA,
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
        db_column='balance',
        editable=False,
    )

    is_locked = models.BooleanField(default=False)
    locked_reason = models.CharField(max_length=1024, blank=True, default='')

    def __str__(self):
        return f'{self.uid} - {self.currency}'

    class Meta:
        unique_together = ('account', 'profile', 'currency')

    @property
    def balance(self) -> Decimal:
        return self._balance

    def get_sum_of_total_disbursements(self) -> Decimal:
        """
        Get sum of total disbursements
        """
        _qs = self.transactions.filter(tx_type='debit', category='disbursement').exclude(is_reversal=True)
        return _qs.aggregate(total=models.Sum('amount', default=Decimal('0'))).get(
            'total', Decimal(0),
        ) or Decimal(0)

    def create_transaction_record(
        self,
        provider_tx_id,
        destination,
        tx_type,
        amount,
        status,
        **kwargs,
    ) -> Transaction:
        return self.transactions.create(
            provider_tx_id=provider_tx_id,
            account=self.account,
            destination=destination,
            tx_type=tx_type,
            amount=amount,
            status=status,
            previous_balance=kwargs.get('previous_balance', None),
            metadata=kwargs.get('metadata', None),
        )

    def credit(
        self,
        provider_tx_id: str,
        category: str,
        amount: Decimal,
        **kwargs,
    ) -> Transaction:
        transaction_type: str = TransactionType.CREDIT

        with transaction.atomic():
            __balance = self._balance

            transaction = self.create_transaction_record(
                provider_tx_id=provider_tx_id,
                destination='self',
                tx_type=transaction_type,
                category=category,
                amount=amount,
                status=TransactionStatus.SUCCESSFUL,
                previous_balance = __balance,
                metadata=kwargs.get('metadata', None),
            )
            self._balance = models.F('_balance') + amount
            self.save()

        return transaction

    def pre_debit(
        self,
        provider_tx_id: str,
        category: str,
        amount: Decimal,
        destination: str,
        **kwargs,
    ) -> Transaction:
        transaction_type: str = TransactionType.CREDIT
        transaction_status: str = TransactionStatus.PENDING

        if self.is_locked:
            raise ValidationError(
                'Wallet is locked',
                code='wallet_locked',
            )
        return self.create_transaction_record(
            provider_tx_id=provider_tx_id,
            amount=amount,
            status=transaction_status,
            tx_type=transaction_type,
            category=category,
            destination=destination,
            metadata=kwargs.get('metadata', None),
        )

    def debit(
        self,
        transaction: Transaction,
    ) -> None:

        if transaction.wallet == self and transaction.status == TransactionStatus.SUCCESSFUL:
            self._balance = models.F('_balance') + transaction.amount
            self.save()
        else:
            raise ValidationError(
                'Transaction not successful',
                code='transaction_not_successful',
            )




