from django.core.urlresolvers import reverse
from django.utils.dateformat import format

from chouwa.decorators import jinjaglobal, jinjafilter

@jinjaglobal
def url(viewname, *args, **kwargs):
    '''
    Lookup a url via `django.core.urlresolvers.reverse`.

    :Parameters:
      viewname : str
        The label associated with a url or the dotted path module name
        of a view.
    '''

    return reverse(viewname, *args, **kwargs)

@jinjafilter
def date(value, format_string):
    return format(value, format_string)
