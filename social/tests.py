# Django
from django.template import Context, Template
from django.test import TestCase
from django.test.client import RequestFactory

# First Party
from pages.models import Page

# Locals
from .templatetags.social_tags import get_breadcrumbs, jsonld


class TestSiteMessages(TestCase):
    def test_jsonld(self):
        data = [{"@context": "http://schema.org", "@type": "LocalBusiness", "name": "mock business"}]

        expected = (
            '<script type="application/ld+json">[{'
            '"@context": "http://schema.org", '
            '"@type": "LocalBusiness", '
            '"name": "mock business"'
            "}]</script>"
        )
        got = jsonld(data)

        self.assertEqual(got, expected)

    def test_jsonld_indented(self):
        data = [{"@context": "http://schema.org", "@type": "LocalBusiness", "name": "mock business"}]

        expected = """<script type="application/ld+json">[
 {
  "@context": "http://schema.org",
  "@type": "LocalBusiness",
  "name": "mock business"
 }
]</script>"""
        got = jsonld(data, True)

        self.assertEqual(got, expected)

    def test_breadcrumbs(self):
        root = Page.add_root(title="root")
        prev = root
        for i in range(5):
            prev = prev.add_child(title=f"level {i}")

        crumbs = get_breadcrumbs(prev.get_ancestors())

        expected = [
            {"@type": "ListItem", "position": 1, "item": {"@id": "root", "name": "root"}},
            {"@type": "ListItem", "position": 2, "item": {"@id": "level 0", "name": "level 0"}},
            {"@type": "ListItem", "position": 3, "item": {"@id": "level 1", "name": "level 1"}},
            {"@type": "ListItem", "position": 4, "item": {"@id": "level 2", "name": "level 2"}},
            {"@type": "ListItem", "position": 5, "item": {"@id": "level 3", "name": "level 3"}},
        ]

        self.assertEqual(list(crumbs), expected)

    def test_empty_social_tags(self):
        factory = RequestFactory()
        request = factory.get("/")
        context = Context({"request": request})
        template = Template("{% load social_tags %}{% social_tags %}")

        got = template.render(context)
        expected = """<meta property="og:type" content="website" />
<meta property="og:url" content="http://localhost" />"""

        self.assertHTMLEqual(got, expected)
