from django.core.management.base import BaseCommand

from wagtail.models import Page


class Command(BaseCommand):
    help = "Sets all live pages to be in the nav"

    def handle(self, *args, **options):
        for page in Page.objects.filter(live=True):
            page.show_in_menus = True
            page.save()
            self.stdout.write(self.style.SUCCESS(f"{page.title} is now in the nav"))
