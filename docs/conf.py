# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import tomlkit

topdir = os.path.split(os.path.split(__file__)[0])[0]
sys.path.insert(0, topdir)
from edgegraph import version as eg_version

with open(os.path.join(topdir, "pyproject.toml"), 'r') as ppyfile:
    pyproject = tomlkit.parse(ppyfile.read())

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'edgegraph'
copyright = '2023, Misha Turnbull'
author = 'Misha Turnbull'
version = f'v{eg_version.VERSION_MAJOR}.{eg_version.VERSION_MINOR}'
release = eg_version.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

primary_domain = "py"
keep_warnings = True
nitpicky = True

extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.autosummary',
        'sphinx.ext.intersphinx',
        'sphinx.ext.todo',
        'sphinxcontrib.plantuml',
        'sphinx_copybutton',
        ]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'README.md']

rst_prolog = """
.. role:: python(code)
   :language: python
"""

# -- Options for InterSphinx -------------------------------------------------

intersphinx_mapping = {
        'python': ('https://docs.python.org/3', None),
        }

# -- Options for autodoc / autosummary ---------------------------------------

# may be "both", "signature", "description", or "none"
autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"
autodoc_typehints_format = "short"
autosummary_generate = True

# -- Options for ToDo ext ----------------------------------------------------

todo_include_todos = True

# -- Options for PlantUML ----------------------------------------------------

plantuml_output_format = "svg"
plantuml_latex_output_format = "pdf"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']

html_theme_options = {
        "repository_url": pyproject['project']['urls']['Repository'],
        "path_to_docs": "docs",
        "use_repository_button": True,
        "use_source_button": True,
        "use_edit_page_button": True,
        "use_issues_button": True,
        }

if eg_version.VERSION_MAJOR == 0:
    html_theme_options["announcement"] = \
            f"<b style=\"color:red;\">edgegraph is in unstable version " \
            f"{version}, and may change at any time!</b>"

