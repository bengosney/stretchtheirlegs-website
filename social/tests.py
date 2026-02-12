from django.template import Context, Template
from django.test import TestCase
from django.test.client import RequestFactory

from wagtail.models import Site

from pages.models import Page
from social.templatetags.social_tags import get_breadcrumbs, jsonld


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
        Site.objects.create(hostname="example.com", root_page=root, is_default_site=True)
        prev = root
        for i in range(5):
            prev = prev.add_child(title=f"level {i}")

        crumbs = list(get_breadcrumbs(prev.get_ancestors()))

        expected = [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "root",
                "item": "http://example.com/",
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "level 0",
                "item": "http://example.com/level-0/",
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": "level 1",
                "item": "http://example.com/level-0/level-1/",
            },
            {
                "@type": "ListItem",
                "position": 4,
                "name": "level 2",
                "item": "http://example.com/level-0/level-1/level-2/",
            },
            {
                "@type": "ListItem",
                "position": 5,
                "name": "level 3",
                "item": "http://example.com/level-0/level-1/level-2/level-3/",
            },
        ]

        for i, crumb in enumerate(crumbs):
            self.assertEqual(crumb, expected[i])

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
