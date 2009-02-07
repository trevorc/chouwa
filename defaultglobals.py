# defaultglobals.py
#
# Copyright (c) 2009 Trevor Caira
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
