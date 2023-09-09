# Generated by Django 4.2.5 on 2023-09-09 11:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
        migrations.AddField(
            model_name='account',
            name='customer_id',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='customer id'),
        ),
        migrations.AddField(
            model_name='account',
            name='deposit_account_id',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='deposit account id'),
        ),
    ]
