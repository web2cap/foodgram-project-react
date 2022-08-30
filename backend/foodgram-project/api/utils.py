import os
from io import BytesIO

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import get_template
from xhtml2pdf import pisa


def fetch_pdf_resources(uri, rel=None):
    if uri.find(settings.MEDIA_URL) != -1:
        path = os.path.join(
            settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, "")
        )
    elif uri.find(settings.STATIC_URL) != -1:
        path = os.path.join(
            settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, "")
        )
    else:
        path = None
    return path


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)

    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(
        BytesIO(html.encode("UTF-8")),
        result,
        encoding="utf-8",
        link_callback=fetch_pdf_resources,
    )
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return HttpResponseBadRequest()
