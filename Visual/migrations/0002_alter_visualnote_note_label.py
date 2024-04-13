# Generated by Django 5.0.2 on 2024-04-09 15:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Visual", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="visualnote",
            name="note_label",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="Visual.visuallabel",
            ),
        ),
    ]