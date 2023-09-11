# Generated by Django 4.2.5 on 2023-09-11 22:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_alter_wallet_account_alter_wallet_profile'),
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='anchor_tx_id',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='id',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='source',
        ),
        migrations.AddField(
            model_name='transaction',
            name='account',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='transactions',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name='transaction',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='deleted at'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='previous_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='previous balance'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='provider_tx_id',
            field=models.CharField(
                default='adddddd', max_length=250, unique=True, verbose_name='provider transaction id'
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='wallet',
            field=models.ForeignKey(
                default='',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='transactions',
                to='accounts.wallet',
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
    ]