# Generated by Django 5.1.3 on 2024-11-14 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_alter_transaction_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
