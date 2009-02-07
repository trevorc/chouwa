'''
Create a Jinja2 Environment object and 

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
