# Generated by Django 4.1.7 on 2023-07-31 07:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("web", "0019_remove_massage_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="main_concern",
            field=models.CharField(blank=True, default="", max_length=200, null=True),
        ),
    ]