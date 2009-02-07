# environment.py
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

'''
Create a Jinja2 Environment object and install filters and globals.

Requires a django setting `PROJECT_ROOT` which the parent directory of a
directory called "templates" which contains the site-wide common
templates.

'''

from itertools import chain
import os
import sys

from django.conf import settings
from django.template.loaders.app_directories import app_template_dirs
from django.utils.translation import ugettext, ungettext
from jinja2 import Environment, FileSystemLoader
from jinja2.ext import i18n

from chouwa import defaultglobals

class DjangoTranslator(object):
    ungettext = ungettext
    ugettext = ugettext

def get_app_modules():
    '''
    Generator yielding module objects containing application-specific
    jinjaglobals. Note that the globals are not namespaced for the
    application.

    '''

    for app_label in settings.INSTALLED_APPS:
        mod_name = '.'.join((app_label, 'jinjaglobals'))
        try:
            __import__(mod_name, {}, {}, [], 0)
            yield sys.modules[mod_name]
        except ImportError:
            pass

def install_globals(env):
    '''
    Add the default filters and globals to the jinja2 environment.

    :Parameters:
      env : `jinja2.Environment`
        The jinja2 environment.

    '''

    for mod in chain((defaultglobals,), get_app_modules()):
        for name in dir(mod):
            global_ = getattr(mod, name)
            if getattr(global_, 'is_jinja_global', False):
                env.globals[name] = global_
            elif getattr(global_, 'is_jinja_filter', False):
                env.filters[name] = global_

def make_environment():
    '''
    Create and populate the jinja2 environment.

    '''

    searchpath = (os.path.join(settings.PROJECT_ROOT, 'templates'),) + \
                 app_template_dirs
    env = Environment(loader=FileSystemLoader(searchpath),
                      autoescape=True, extensions=(i18n,),
                      auto_reload=settings.TEMPLATE_DEBUG)
    install_globals(env)
    env.install_gettext_translations(DjangoTranslator())
    return env

env = make_environment()
