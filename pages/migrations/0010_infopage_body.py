# Generated by Django 4.0.4 on 2022-05-07 20:59

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_remove_sitesettings_google_maps_api_key_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='infopage',
            name='body',
            field=wagtail.fields.StreamField([('Paragraph', wagtail.blocks.RichTextBlock()), ('Services', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(max_length=255, required=True)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('services', wagtail.blocks.ListBlock(wagtail.blocks.PageChooserBlock(page_type=['pages.ServicePage'])))]))], default=''),
            preserve_default=False,
        ),
    ]
