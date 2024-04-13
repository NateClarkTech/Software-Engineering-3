# Generated by Django 5.0.2 on 2024-04-09 15:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="VisualLabel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("label_name", models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name="VisualNote",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("note_title", models.CharField(max_length=30)),
                ("note_description", models.CharField(max_length=1200)),
                ("note_image", models.ImageField(default=None, upload_to="images/")),
                (
                    "note_label",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Visual.visuallabel",
                    ),
                ),
            ],
        ),
    ]