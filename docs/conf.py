# -- Path setup --------------------------------------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../src'))


# -- Project information -----------------------------------------------------

project = 'dahlia'
copyright = '2022, trag1c'
author = 'trag1c'

release = '0.1.0'


# -- General configuration ---------------------------------------------------


extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx'
]


exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


html_theme = 'piccolo_theme'

pygments_style = "one-dark"


html_static_path = ['_static']
html_css_files = [
    'dahlia.css'
]
html_js_files = [
    'dahlia.js'
]

# -- Extension configuration -------------------------------------------------

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

autodoc_typehints_format = 'short'
