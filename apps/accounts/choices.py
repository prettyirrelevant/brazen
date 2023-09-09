from django.db import models


class Country(models.TextChoices):
    NIGERIA = 'NG'


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
