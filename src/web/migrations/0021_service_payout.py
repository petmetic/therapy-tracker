# Generated by Django 4.1.7 on 2023-09-04 11:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("web", "0020_customer_main_concern"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="payout",
            field=models.IntegerField(default=50, null=True),
        ),
    ]