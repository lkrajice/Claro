# -*- coding: utf-8 -*-
import os
import sys

import django
import sphinx_rtd_theme

# import claro functions
sys.path.insert(0, os.path.join('..', '..'))
from claro import get_version

# Need to setup django first before documenting
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "claro.settings")
django.setup()

# -- Project information -----------------------------------------------------
project = u'Claro'
copyright = u'2018, Lukáš Krajíček, Filip Bartoš'
author = u'Lukáš Krajíček, Filip Bartoš'
version, release = get_version()

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]


# Paths to directories containings templates
templates_path = ['_templates']

# List of suffixes used for source files
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# Language for sphynx documents
language = 'en'

# Excludes patterns for source files
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- HTML --------------------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Paths to directories containings static files
html_static_path = ['_static']

# Napoleon setting
napoleon_google_docstring = True
napoleon_use_param = True
napoleon_use_ivar = True

# -- Todo extension ----------------------------------------------------------

# `todo` and `todoList` is generated
todo_include_todos = True
