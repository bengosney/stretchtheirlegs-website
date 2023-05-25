# Django
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models

# Wagtail
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index

# First Party
from pages.blocks import ImageRow, ItemBlock, ServicesBlock


class ArticleList(Page):
    show_in_menus_default = True
    sub_heading = models.CharField(max_length=255, default="", blank=True)

    body = StreamField(
        [
            ("Paragraph", blocks.RichTextBlock()),
            ("Services", ServicesBlock()),
            ("Item", ItemBlock()),
            ("ImageRow", ImageRow()),
        ],
        use_json_field=True,
    )

    subpage_types = ["articles.Article"]

    content_panels = Page.content_panels + [
        FieldPanel("sub_heading"),
        FieldPanel("body"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        page = request.GET.get("page", 1)

        articles = Article.objects.child_of(self).live()

        paginator = Paginator(articles, 2)
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context["articles"] = articles

        return context


class Article(Page):
    show_in_menus_default = False
    sub_heading = models.CharField(max_length=255, default="", blank=True)

    date = models.DateField("Post date", null=True, blank=True)
    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    body = StreamField(
        [
            ("Paragraph", blocks.RichTextBlock()),
            ("Services", ServicesBlock()),
            ("Item", ItemBlock()),
            ("ImageRow", ImageRow()),
        ],
        use_json_field=True,
    )

    subpage_types = []

    parent_page_types = ["articles.ArticleList"]

    content_panels = Page.content_panels + [
        FieldPanel("sub_heading"),
        FieldPanel("banner_image"),
        FieldPanel("body"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("body"),
        index.FilterField("date"),
    ]
