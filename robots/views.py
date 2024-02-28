# Django
from django.http import HttpResponse

# First Party
from robots.models import Robots


def robots(request):
    robots_txt = Robots.for_request(request)

    return HttpResponse(robots_txt.contents, content_type="text/plain")
