# Generated by Django 5.0.2 on 2024-05-12 16:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("IdeaBoards", "0011_ideaboard_is_public_ideaboarditem_label_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ideaboarditem",
            name="board_image",
        ),
        migrations.RemoveField(
            model_name="ideaboarditem",
            name="board_sound",
        ),
        migrations.RemoveField(
            model_name="ideaboarditem",
            name="label",
        ),
        migrations.AddField(
            model_name="ideaboarditem",
            name="item_image",
            field=models.ImageField(blank=True, null=True, upload_to="item_image/"),
        ),
        migrations.AddField(
            model_name="ideaboarditem",
            name="item_sound",
            field=models.FileField(blank=True, null=True, upload_to="item_sounds/"),
        ),
    ]