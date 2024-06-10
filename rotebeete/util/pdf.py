from django.http import HttpResponse, HttpResponseServerError
from django.template.loader import get_template
from xhtml2pdf import pisa


def render_to_pdf_http(template_name, renderdict, filename):
    """
    Take a string of rendered html and pack it
    into a pdf and return it through http
    """
    rendered_html = get_template(template_name).render(renderdict)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="' + filename + '"'

    success = pisa.CreatePDF(rendered_html, dest=response)

    if not success:
        return HttpResponseServerError()
    return response
