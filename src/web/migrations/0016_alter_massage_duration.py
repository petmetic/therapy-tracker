# Generated by Django 4.1.7 on 2023-05-10 16:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("web", "0015_alter_service_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="massage",
            name="duration",
            field=models.IntegerField(default=0, null=True),
        ),
    ]
