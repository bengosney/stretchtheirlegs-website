# Generated by Django 4.0.4 on 2022-05-21 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OGTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(choices=[('type', 'Type'), ('title', 'Title'), ('description', 'Description'), ('image', 'Image'), ('url', 'URL'), ('site_name', 'Site Name')], max_length=100)),
                ('content', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'OG Tag',
                'verbose_name_plural': 'OG Tags',
            },
        ),
    ]
