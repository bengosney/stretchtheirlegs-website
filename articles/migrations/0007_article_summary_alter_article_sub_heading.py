# Generated by Django 4.2.1 on 2023-05-30 20:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0006_rename_image_article_banner_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="summary",
            field=models.CharField(blank=True, default="", max_length=200),
        ),
        migrations.AlterField(
            model_name="article",
            name="sub_heading",
            field=models.CharField(blank=True, default="", max_length=50),
        ),
    ]