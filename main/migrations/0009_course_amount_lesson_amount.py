# Generated by Django 4.2.7 on 2023-12-03 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_payment_stripe_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='amount',
            field=models.CharField(blank=True, null=True, verbose_name='amount'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='amount',
            field=models.CharField(blank=True, null=True, verbose_name='amount'),
        ),
    ]
