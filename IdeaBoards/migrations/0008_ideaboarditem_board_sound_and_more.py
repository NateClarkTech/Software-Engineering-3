# Generated by Django 5.0.2 on 2024-05-01 03:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("IdeaBoards", "0007_alter_ideaboarditem_board_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="ideaboarditem",
            name="board_sound",
            field=models.FileField(default=1, upload_to="board_sounds/"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="ideaboarditem",
            name="board_image",
            field=models.ImageField(blank=True, upload_to="board_image/"),
        ),
    ]
