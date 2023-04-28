import os
import sys

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../mexa'))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Mexa'
copyright = '2023 Miguel Angel Marcial Martínez'
author = 'Miguel Angel Marcial Martínez'

##
html_context = {
    "display_github": True, # Muestra el enlace de GitHub
    "github_user": "fitorec", # Nombre de usuario de GitHub
    "github_repo": "mexa-py", # Nombre del repositorio de GitHub
    "github_version": "main/doc/", # La ruta de la documentación en el repositorio
    "conf_py_path": "/doc_src/", # El directorio de la documentación en tu repositorio
}

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc',
#    'sphinx_markdown_builder',
    'myst_parser'
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = 'mundosica'
html_theme_path = ['_themes']
html_static_path = ['_static']
html_domain_indices = ['mexa']

#
language = 'es'

