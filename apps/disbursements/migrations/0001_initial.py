# Generated by Django 4.2.5 on 2023-09-13 04:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Beneficiary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='updated at')),
                ('tag', models.CharField(blank=True, max_length=150, null=True, verbose_name='tag')),
                ('account_number', models.CharField(max_length=11)),
                ('account_name', models.CharField(max_length=150)),
                ('anchor_bank_code', models.CharField(max_length=150)),
                ('anchor_bank_id', models.CharField(max_length=150)),
                ('anchor_counterparty_id', models.CharField(max_length=150)),
                (
                    'account',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='beneficiaries',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Disbursement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='updated at')),
                ('description', models.TextField(blank=True, null=True)),
                ('start_at', models.DateTimeField(verbose_name='start at')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                (
                    'currency',
                    models.CharField(
                        choices=[('NGN', 'Naira'), ('USD', 'Dollar')], max_length=3, verbose_name='currency'
                    ),
                ),
                (
                    'frequency',
                    models.CharField(
                        choices=[
                            ('Thirty Minutes', 'Thirty Mins'),
                            ('Hourly', 'Hourly'),
                            ('Weekly', 'Weekly'),
                            ('Biweekly', 'Biweekly'),
                            ('Monthly', 'Monthly'),
                        ],
                        default='Thirty Minutes',
                        max_length=15,
                    ),
                ),
                (
                    'status',
                    models.CharField(
                        choices=[('active', 'Active'), ('inactive', 'Inactive')],
                        default='active',
                        max_length=20,
                        verbose_name='status',
                    ),
                ),
                (
                    'account',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='disbursements',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'beneficiary',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='disbursements',
                        to='disbursements.beneficiary',
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DisbursementEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='updated at')),
                ('retries', models.IntegerField(default=0, verbose_name='retries')),
                ('run_at', models.DateTimeField(verbose_name='run at')),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('failure', 'Failure'),
                            ('pending', 'Pending'),
                            ('success', 'Success'),
                            ('not started', 'Not Started'),
                        ],
                        max_length=20,
                        verbose_name='status',
                    ),
                ),
                (
                    'disbursement',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='events',
                        to='disbursements.disbursement',
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='beneficiary',
            constraint=models.UniqueConstraint(
                fields=('account', 'account_number'), name='account_and_account_number_unique'
            ),
        ),
    ]
