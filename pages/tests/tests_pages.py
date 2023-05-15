# Django

# Wagtail
from wagtail.models import Page
from wagtail.test.utils import WagtailPageTestCase

# Locals
from ..models import InfoPage


class ParentToolTests(WagtailPageTestCase):
    def test_get_parent_title(self):
        root = Page.add_root(instance=Page(title="root", path="/"))
        child = root.add_child(instance=InfoPage(title="child", path="/child"))

        self.assertEqual(child.parent_title, "root")

    def test_get_parent_title_site_root(self):
        root = Page.add_root(instance=Page(title="root", path="/"))
        root._is_site_root = True
        child = root.add_child(instance=InfoPage(title="child", path="/child"))

        self.assertEqual(child.parent_title, None)
