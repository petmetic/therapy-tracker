# Generated by Django 4.1.7 on 2023-04-24 15:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("web", "0006_massage_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="massage",
            name="service",
            field=models.CharField(blank=True, default="", max_length=200),
        ),
    ]
