from django.http import HttpResponseNotFound, HttpResponseServerError

from chouwa.loader import get_template

def page_not_found(request, template_name='404.html'):
    t = get_template(template_name)
    return HttpResponseNotFound(t.render({'request_path': request.path}))

def server_error(request, template_name='500.html'):
    t = get_template(template_name)
    return HttpResponseServerError(t.render())
