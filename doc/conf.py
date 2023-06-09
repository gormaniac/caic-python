import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

project = 'caic-python'
copyright = '2023, John Gorman'
author = 'John Gorman'

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.githubpages']

templates_path = ['_templates']
exclude_patterns = []


html_theme = 'sphinx_rtd_theme'
html_static_path = []
# html_sidebars = {
#     '**': [
#         'relations.html',  # needs 'show_related': True theme option to display
#         'searchbox.html',
#     ]
# }
