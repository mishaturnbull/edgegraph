# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

topdir = os.path.split(os.path.split(__file__)[0])[0]
sys.path.insert(0, topdir)
from edgegraph import version as eg_version


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'edgegraph'
copyright = '2023, Misha Turnbull'
author = 'Misha Turnbull'
version = f'v{eg_version.VERSION_MAJOR}.{eg_version.VERSION_MINOR}'
release = eg_version.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

primary_domain = "python"
keep_warnings = True
nitpicky = True

extensions = [
        'sphinx.ext.intersphinx',
        'sphinxcontrib.plantuml',
        'sphinx_copybutton',
        ]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'README.md']

# -- Options for InterSphinx -------------------------------------------------

intersphinx_mapping = {
        'python': ('https://docs.python.org/3', None),
        }

# -- Options for PlantUML ----------------------------------------------------

plantuml_output_format = "png"
plantuml_latex_output_format = "pdf"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']

html_theme_options = {
        }

if eg_version.VERSION_MAJOR == 0:
    html_theme_options["announcement"] = \
            f"<b style=\"color:red;\">edgegraph is in unstable version " \
            f"{version}, and may change at any time!</b>"

