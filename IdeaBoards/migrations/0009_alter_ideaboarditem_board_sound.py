# Generated by Django 5.0.2 on 2024-05-01 17:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("IdeaBoards", "0008_ideaboarditem_board_sound_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ideaboarditem",
            name="board_sound",
            field=models.FileField(blank=True, upload_to="board_sounds/"),
        ),
    ]