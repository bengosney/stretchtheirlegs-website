# Generated by Django 4.2.1 on 2023-05-17 12:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("logos", "0006_alter_logo_effect"),
    ]

    operations = [
        migrations.AlterField(
            model_name="logo",
            name="effect",
            field=models.CharField(
                blank=True,
                choices=[("snow", "Snow"), ("fireworks", "Fireworks"), ("confetti", "Confetti"), ("explosions", "Explosions")],
                default=None,
                max_length=10,
                null=True,
                verbose_name="Effect",
            ),
        ),
    ]
