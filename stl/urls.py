from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path("sitemap.xml", sitemap),
    path("admin/", include(wagtailadmin_urls)),
    path("django-admin/", admin.site.urls),
    path("documents/", include(wagtaildocs_urls)),
    path("messages/", include("site_messages.urls", namespace="site_messages")),
    path("robots.txt", include("robots.urls")),
]


if settings.DEBUG:
    # Django
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.SCSS_SOURCEMAP_URL, document_root=settings.SCSS_SOURCEMAP_ROOT)
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)

# For anything not caught by a more specific rule above, hand over to
# Wagtail's page serving mechanism. This should be the last pattern in
# the list:
urlpatterns = [
    *urlpatterns,
    path("", include(wagtail_urls)),
]
