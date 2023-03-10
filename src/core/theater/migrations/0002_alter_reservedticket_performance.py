# Generated by Django 4.1.5 on 2023-01-05 12:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("theater", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservedticket",
            name="performance",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="reserved_tickets", to="theater.performance"
            ),
        ),
    ]
