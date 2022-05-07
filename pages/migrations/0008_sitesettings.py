# Generated by Django 4.0.4 on 2022-05-07 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0066_collection_management_permissions'),
        ('pages', '0007_membership'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(default='', help_text='Phone number to show in the footer', max_length=255)),
                ('facebook', models.URLField(default='', help_text='Your Facebook page URL')),
                ('instagram', models.CharField(default='', help_text='Your Instagram username, without the @', max_length=255)),
                ('google_maps_api_key', models.CharField(default='', help_text='Google Maps API key', max_length=255)),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
