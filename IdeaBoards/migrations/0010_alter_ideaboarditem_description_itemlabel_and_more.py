# Generated by Django 5.0.2 on 2024-05-02 14:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("IdeaBoards", "0009_alter_ideaboarditem_board_sound"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ideaboarditem",
            name="description",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.CreateModel(
            name="ItemLabel",
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
                (
                    "label_board",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="IdeaBoards.ideaboard",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="ideaboarditem",
            name="note_label",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="IdeaBoards.itemlabel",
            ),
        ),
    ]
