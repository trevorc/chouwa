# Based on djangojinja2.py by Armin Ronacher.

from django.template import TemplateDoesNotExist
from django.template.context import get_standard_processors
from jinja2 import TemplateNotFound

from chouwa.environment import env

def get_template(template_name, globals=None):
    """Load a template."""
    try:
        return env.get_template(template_name, globals=globals)
    except TemplateNotFound, e:
        raise TemplateDoesNotExist(str(e))

def select_template(templates, globals=None):
    """Try to load one of the given templates."""
    for template in templates:
        try:
            return env.get_template(template, globals=globals)
        except TemplateNotFound:
            continue
    raise TemplateDoesNotExist(', '.join(templates))

def render_to_string(template_name, context=None, request=None):
    """Render a template into a string."""
    if context is None:
        context = {}
    if request is not None:
        context['request'] = request
        for processor in get_standard_processors():
            context.update(processor(request))
    return get_template(template_name).render(context)
