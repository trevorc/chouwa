from django.http import HttpResponse

from chouwa.loader import render_to_string

def direct_to_template(request, template, extra_context=None,
                       mimetype=None):
    return HttpResponse(render_to_string(template, extra_context),
                        mimetype=mimetype)
