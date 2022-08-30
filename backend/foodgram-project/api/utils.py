import io
from html import escape

from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict):
    html = render_to_string(template_src, context_dict)
    result = io.BytesIO()

    pdf = pisa.pisaDocument(io.BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return HttpResponse("We had some errors<pre>%s</pre>" % escape(html))
