# Generated by Django 4.1.7 on 2023-05-03 14:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("web", "0009_alter_service_time_before"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="time_after",
            field=models.IntegerField(default=0),
        ),
    ]
