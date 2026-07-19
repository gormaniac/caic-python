import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

project = 'CAIC Python'
copyright = '2023, John Gorman'
author = 'John Gorman'

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = []

html_theme = "shibuya"
html_static_path = ["_static"]
html_title = "CAIC Python Docs"

html_baseurl = 'https://docs.gormo.co/caic-python/'

html_theme_options = {
    "accent_color": "teal",
    "color_mode": "auto",
    "nav_socials": [
        {
            "name": "GitHub",
            "url": "https://github.com/gormaniac/caic-python",
            "icon": "simple-icons:github",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/caic-python/",
            "icon": "simple-icons:pypi",
        },
    ],
    "foot_socials": [
        {
            "name": "GitHub",
            "url": "https://github.com/gormaniac/caic-python",
            "icon": "simple-icons:github",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/caic-python/",
            "icon": "simple-icons:pypi",
        },
    ]
}
