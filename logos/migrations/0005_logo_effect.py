# Generated by Django 4.2.1 on 2023-05-15 07:41

from django.db import migrations, models

from icecream import ic


def copy_effects(apps, schema_editor):
    Logo = apps.get_model("logos", "logo")

    try:
        manager_name = Logo._meta.default_manager_name
    except AttributeError:
        manager_name = "objects"

    for logo in getattr(Logo, manager_name).all():
        if logo.snow:
            logo.effect = "snow"
        if logo.fireworks:
            logo.effect = "fireworks"

        logo.save()


class Migration(migrations.Migration):
    dependencies = [
        ("logos", "0004_logo_snow"),
    ]

    operations = [
        migrations.AddField(
            model_name="logo",
            name="effect",
            field=models.CharField(
                blank=True,
                choices=[("snow", "Snow"), ("fireworks", "Fireworks")],
                default=None,
                null=True,
                max_length=9,
                verbose_name="Effect",
            ),
        ),
        migrations.RunPython(copy_effects),
        migrations.RemoveField(
            model_name="logo",
            name="fireworks",
        ),
        migrations.RemoveField(
            model_name="logo",
            name="snow",
        ),
    ]
