# Create your views here.
# Standard Library
import contextlib

# Django
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect

# Locals
from .models import Message


def dismiss(request, slug):
    with contextlib.suppress(ObjectDoesNotExist):
        m = Message.objects.get(slug=slug)
        m.dismiss(request.session)

    url = request.headers.get("Referer", "/")

    return HttpResponseRedirect(url)
