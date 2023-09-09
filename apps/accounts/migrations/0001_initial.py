# Generated by Django 4.2.5 on 2023-09-09 13:53

import apps.accounts.managers
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                (
                    'is_superuser',
                    models.BooleanField(
                        default=False,
                        help_text='Designates that this user has all permissions without explicitly assigning them.',
                        verbose_name='superuser status',
                    ),
                ),
                (
                    'is_staff',
                    models.BooleanField(
                        default=False,
                        help_text='Designates whether the user can log into this admin site.',
                        verbose_name='staff status',
                    ),
                ),
                (
                    'is_active',
                    models.BooleanField(
                        default=True,
                        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
                        verbose_name='active',
                    ),
                ),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('first_name', models.CharField(max_length=150, verbose_name='first name')),
                ('phone_number', models.CharField(max_length=11, unique=True, verbose_name='phone number')),
                ('address', models.TextField(verbose_name='address')),
                ('city', models.CharField(max_length=100, verbose_name='city')),
                ('postal_code', models.IntegerField(verbose_name='postal code')),
                (
                    'gender',
                    models.CharField(
                        choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')],
                        max_length=20,
                        verbose_name='gender',
                    ),
                ),
                (
                    'country',
                    models.CharField(choices=[('NG', 'Nigeria')], default='NG', max_length=10, verbose_name='country'),
                ),
                (
                    'state',
                    models.CharField(
                        choices=[
                            ('FCT', 'Fct'),
                            ('OYO', 'Oyo'),
                            ('IMO', 'Imo'),
                            ('EDO', 'Edo'),
                            ('KANO', 'Kano'),
                            ('ONDO', 'Ondo'),
                            ('OSUN', 'Osun'),
                            ('OGUN', 'Ogun'),
                            ('KOGI', 'Kogi'),
                            ('YOBE', 'Yobe'),
                            ('ABIA', 'Abia'),
                            ('ENUGU', 'Enugu'),
                            ('LAGOS', 'Lagos'),
                            ('NIGER', 'Niger'),
                            ('BENUE', 'Benue'),
                            ('GOMBE', 'Gombe'),
                            ('KWARA', 'Kwara'),
                            ('EKITI', 'Ekiti'),
                            ('DELTA', 'Delta'),
                            ('BORNO', 'Borno'),
                            ('KEBBI', 'Kebbi'),
                            ('KADUNA', 'Kaduna'),
                            ('BAUCHI', 'Bauchi'),
                            ('EBONYI', 'Ebonyi'),
                            ('JIGAWA', 'Jigawa'),
                            ('SOKOTO', 'Sokoto'),
                            ('RIVERS', 'Rivers'),
                            ('TARABA', 'Taraba'),
                            ('ZAMFARA', 'Zamfara'),
                            ('PLATEAU', 'Plateau'),
                            ('ADAMAWA', 'Adamawa'),
                            ('ANAMBRA', 'Anambra'),
                            ('KATSINA', 'Katsina'),
                            ('BAYELSA', 'Bayelsa'),
                            ('NASARAWA', 'Nasarawa'),
                            ('AKWA_IBOM', 'Akwa Ibom'),
                            ('CROSS_RIVER', 'Cross River'),
                        ],
                        max_length=20,
                        verbose_name='state',
                    ),
                ),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                (
                    'deposit_account_id',
                    models.CharField(blank=True, max_length=150, null=True, verbose_name='deposit account id'),
                ),
                (
                    'deposit_account_number',
                    models.CharField(blank=True, max_length=11, null=True, verbose_name='deposit account number'),
                ),
                (
                    'deposit_bank_name',
                    models.CharField(blank=True, max_length=150, null=True, verbose_name='deposit bank name'),
                ),
                ('customer_id', models.CharField(blank=True, max_length=150, null=True, verbose_name='customer id')),
                (
                    'groups',
                    models.ManyToManyField(
                        blank=True,
                        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                        related_name='user_set',
                        related_query_name='user',
                        to='auth.group',
                        verbose_name='groups',
                    ),
                ),
                (
                    'user_permissions',
                    models.ManyToManyField(
                        blank=True,
                        help_text='Specific permissions for this user.',
                        related_name='user_set',
                        related_query_name='user',
                        to='auth.permission',
                        verbose_name='user permissions',
                    ),
                ),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', apps.accounts.managers.AccountManager()),
            ],
        ),
    ]
