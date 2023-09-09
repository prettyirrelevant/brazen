# Generated by Django 4.2.5 on 2023-09-09 12:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0003_account_deposit_account_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='gender',
            field=models.CharField(
                choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')],
                default='',
                max_length=20,
                verbose_name='gender',
            ),
            preserve_default=False,
        ),
    ]