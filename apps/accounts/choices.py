from django.db import models


class Country(models.TextChoices):
    NIGERIA = 'NG'

class WalletCurrency(models.TextChoices):
    NAIRA = 'NGN'
    DOLLAR = 'USD'


class Currency(models.TextChoices):
    NAIRA = 'NGN'
    DOLLAR = 'USD'


class KYC(models.TextChoices):
    TIER_1 = 'TIER_1'
    TIER_2 = 'TIER_2'
    TIER_3 = 'TIER_3'


class KYCTierThreeDocumentType(models.TextChoices):
    NIN_SLIP = 'NIN_SLIP'
    PASSPORT = 'PASSPORT'
    VOTERS_CARD = 'VOTERS_CARD'
    NATIONAL_ID = 'NATIONAL_ID'
    DRIVERS_LICENSE = 'DRIVERS_LICENSE'


class Gender(models.TextChoices):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHERS = 'Others'


class State(models.TextChoices):
    FCT = 'FCT'
    OYO = 'OYO'
    IMO = 'IMO'
    EDO = 'EDO'
    KANO = 'KANO'
    ONDO = 'ONDO'
    OSUN = 'OSUN'
    OGUN = 'OGUN'
    KOGI = 'KOGI'
    YOBE = 'YOBE'
    ABIA = 'ABIA'
    ENUGU = 'ENUGU'
    LAGOS = 'LAGOS'
    NIGER = 'NIGER'
    BENUE = 'BENUE'
    GOMBE = 'GOMBE'
    KWARA = 'KWARA'
    EKITI = 'EKITI'
    DELTA = 'DELTA'
    BORNO = 'BORNO'
    KEBBI = 'KEBBI'
    KADUNA = 'KADUNA'
    BAUCHI = 'BAUCHI'
    EBONYI = 'EBONYI'
    JIGAWA = 'JIGAWA'
    SOKOTO = 'SOKOTO'
    RIVERS = 'RIVERS'
    TARABA = 'TARABA'
    ZAMFARA = 'ZAMFARA'
    PLATEAU = 'PLATEAU'
    ADAMAWA = 'ADAMAWA'
    ANAMBRA = 'ANAMBRA'
    KATSINA = 'KATSINA'
    BAYELSA = 'BAYELSA'
    NASARAWA = 'NASARAWA'
    AKWA_IBOM = 'AKWA_IBOM'
    CROSS_RIVER = 'CROSS_RIVER'
