# Generated by Django 4.1.7 on 2023-05-02 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("web", "0002_alter_customer_frequency_alter_customer_occupation_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="massage",
            name="massage_name",
            field=models.ForeignKey(
                default="",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="web.service",
            ),
        ),
    ]