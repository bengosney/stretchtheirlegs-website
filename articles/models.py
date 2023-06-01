# Standard Library
import re

# Django
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models

# Wagtail
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index

# Third Party
from bs4 import BeautifulSoup

# First Party
from pages.blocks import ImageRow, ItemBlock, ServicesBlock


class ArticleList(Page):
    NPP = 10

    show_in_menus_default = True
    sub_heading = models.CharField(max_length=255, default="", blank=True)
    list_title = models.CharField(max_length=255, default="", blank=True, help_text="This is shown above the actual list")

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
        FieldPanel("list_title"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        page = request.GET.get("page", 1)

        articles = Article.objects.child_of(self).live()

        paginator = Paginator(articles, self.NPP)
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context["articles"] = articles

        return context


class Article(Page):
    MAX_SUMMARY_LENGTH = 200

    show_in_menus_default = False
    sub_heading = models.CharField(max_length=50, default="", blank=True)
    summary = models.CharField(max_length=MAX_SUMMARY_LENGTH, default="", blank=True)

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
        FieldPanel("summary"),
        FieldPanel("banner_image"),
        FieldPanel("body"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("body"),
        index.FilterField("date"),
    ]

    @property
    def summary_length(self):
        return self.MAX_SUMMARY_LENGTH * 0.75

    @property
    def summary_text(self):
        if self.summary:
            return self.summary

        html = self.body.render_as_block()
        bs = BeautifulSoup(html)
        text = bs.get_text()

        for i in range(6):
            for item in bs.select(f"h{i}"):
                item.extract()

        return re.sub(r"\s+", " ", text, 0, re.MULTILINE)
