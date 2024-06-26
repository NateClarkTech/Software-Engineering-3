# Generated by Django 5.0.2 on 2024-04-12 18:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                (
                    "profile_picture",
                    models.ImageField(
                        default="profile_pics/default.png", upload_to="profile_pics"
                    ),
                ),
                ("personal_info", models.TextField(blank=True, max_length=500)),
                ("firstName", models.TextField(blank=True, max_length=25)),
                ("lastName", models.TextField(blank=True, max_length=25)),
                ("displayName", models.BooleanField(default=False)),
                ("email", models.EmailField(blank=True, max_length=100)),
                ("displayEmail", models.BooleanField(default=False)),
                ("phoneNumber", models.CharField(blank=True, max_length=10)),
                ("displayNumber", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
