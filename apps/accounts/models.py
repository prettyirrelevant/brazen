from decimal import Decimal
from typing import ClassVar

from encrypted_model_fields.fields import EncryptedCharField, EncryptedDateField, EncryptedTextField

from django.contrib.auth.models import AbstractUser
from django.db import models, transaction

from apps.disbursements.choices import DisbursementEventStatus
from apps.transactions.choices import TransactionStatus, TransactionType
from apps.transactions.models import Transaction
from common.models import TimestampedModel

from .choices import KYC, Country, Currency, Gender, KYCTierThreeDocumentType, State
from .managers import AccountManager


class Account(AbstractUser):
    username = None

    email = models.EmailField('email address', unique=True, null=False, blank=False)
    last_name = models.CharField('last name', max_length=150, null=False, blank=False)
    first_name = models.CharField('first name', max_length=150, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name')

    objects = AccountManager()


class Profile(TimestampedModel):
    account = models.OneToOneField(
        Account,
        on_delete=models.SET_NULL,
        related_name='profile',
        null=True,
        blank=True,
    )

    # Anchor Customer creation requirements
    address = EncryptedTextField('address', null=True, blank=True)
    city = EncryptedCharField('city', max_length=100, null=True, blank=True)
    postal_code = EncryptedCharField('postal code', max_length=50, null=True, blank=True)
    state = EncryptedCharField('state', max_length=20, choices=State.choices, null=True, blank=True)
    country = models.CharField('country', max_length=10, choices=Country.choices, default=Country.NIGERIA)
    phone_number = EncryptedCharField('phone number', unique=True, max_length=11, null=True, blank=True)

    # KYC Tier Two requirements
    date_of_birth = EncryptedDateField('date of birth', null=True, blank=True)
    bvn = EncryptedCharField('bank verification number', max_length=11, blank=True, null=True)
    gender = models.CharField('gender', max_length=20, choices=Gender.choices, null=True, blank=True)

    # KYC Tier Three requirements
    document_identifier = EncryptedCharField('document identifier', max_length=250, null=True, blank=True)
    document_expiry_date = EncryptedDateField('document expiry date', null=True, blank=True)
    document_type = EncryptedCharField(
        'document type',
        max_length=250,
        choices=KYCTierThreeDocumentType.choices,
        null=True,
        blank=True,
    )

    kyc_level = models.CharField('kyc level', max_length=6, choices=KYC.choices, default=KYC.TIER_1)
    anchor_customer_id = models.CharField('anchor customer id', unique=True, max_length=150, null=True, blank=True)


class Wallet(TimestampedModel):
    account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        related_name='wallets',
        null=True,
        blank=True,
    )
    balance = models.DecimalField('balance', max_digits=20, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField('currency', choices=Currency.choices, max_length=3, null=False, blank=False)

    # todo: make account_number unique?
    bank_name = models.CharField('deposit bank name', max_length=250, null=True, blank=True)
    account_name = models.CharField('deposit account name', max_length=250, null=True, blank=True)
    account_number = models.CharField('deposit account number', max_length=100, null=True, blank=True)

    anchor_deposit_account_id = models.CharField(
        'anchor deposit account id',
        unique=True,
        max_length=150,
        null=False,
        blank=False,
    )

    is_locked = models.BooleanField('is locked', default=False)
    is_locked_reason = models.TextField('is locked reason', null=True, blank=True)

    class Meta:
        constraints: ClassVar[list] = [
            models.UniqueConstraint(
                fields=('account', 'currency'),
                name='unique_wallet_per_user_and_currency',
            ),
        ]

    @transaction.atomic()
    def credit(self, provider_ref: str, amount_in_least_denomination: Decimal, currency: Currency, metadata: dict):
        if currency == Currency.DOLLAR:
            raise ValueError('Dollar top up is not currently supported')

        amount = amount_in_least_denomination / Decimal(100)
        Transaction.objects.create(
            amount=amount,
            metadata=metadata,
            account=self.account,
            anchor_ref=provider_ref,
            tx_type=TransactionType.FUNDING,
            status=TransactionStatus.SUCCESSFUL,
            currency=Currency(metadata['currency']),
        )

        self.balance = models.F('balance') + amount
        self.save()

    @transaction.atomic()
    def debit(self, tx: Transaction, metadata: dict):
        if self.is_locked:
            raise Exception(self.is_locked_reason)  # noqa: TRY002

        tx.metadata = metadata
        tx.status = TransactionStatus.SUCCESSFUL
        tx.disbursement_event.status = DisbursementEventStatus.SUCCESS
        self.balance = models.F('balance') - tx.amount

        tx.save()
        self.save()
        tx.disbursement_event.save()
