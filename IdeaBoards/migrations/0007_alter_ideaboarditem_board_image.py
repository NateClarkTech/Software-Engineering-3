# Generated by Django 5.0.2 on 2024-04-28 23:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("IdeaBoards", "0006_alter_ideaboarditem_board_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ideaboarditem",
            name="board_image",
            field=models.ImageField(blank=True, upload_to="board_image"),
        ),
    ]
