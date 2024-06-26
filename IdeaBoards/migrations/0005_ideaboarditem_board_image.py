# Generated by Django 5.0.2 on 2024-04-28 04:55

import IdeaBoards.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "IdeaBoards",
            "0004_alter_ideaboard_description_alter_ideaboard_title_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="ideaboarditem",
            name="board_image",
            field=models.ImageField(
                blank=True,
                height_field="500",
                upload_to=IdeaBoards.models.user_directory_path,
                width_field="500",
            ),
        ),
    ]
