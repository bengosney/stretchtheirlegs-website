# Generated by Django 4.2.1 on 2023-05-15 20:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("logos", "0005_logo_effect"),
    ]

    operations = [
        migrations.AlterField(
            model_name="logo",
            name="effect",
            field=models.CharField(
                blank=True,
                choices=[("snow", "Snow"), ("fireworks", "Fireworks"), ("confetti", "Confetti")],
                default=None,
                max_length=9,
                null=True,
                verbose_name="Effect",
            ),
        ),
    ]
