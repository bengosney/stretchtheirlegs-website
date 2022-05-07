# Standard Library

# Wagtail
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class ServicesBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, max_length=255)
    body = blocks.RichTextBlock(required=False)
    services = blocks.ListBlock(blocks.PageChooserBlock(target_model="pages.ServicePage"))

    class Meta:
        template = "pages/blocks/services.html"


class FormBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False)

    class Meta:
        template = "pages/blocks/form.html"
        icon = "form"


class ItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, max_length=255)
    sub_title = blocks.CharBlock(required=False, max_length=255)
    image = ImageChooserBlock()
    body = blocks.RichTextBlock()

    class Meta:
        template = "pages/blocks/item.html"
