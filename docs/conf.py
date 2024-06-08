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
from docs._auto import git

with open(os.path.join(topdir, "pyproject.toml"), 'r') as ppyfile:
    pyproject = tomlkit.parse(ppyfile.read())

# -- PyReverse calls ---------------------------------------------------------
# import and run the helper script that generates the plantuml diagrams, which
# are then rendered by sphinx-plantuml.

from docs._scripts import pyrev_helper
pyrev_helper.main()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'edgegraph'
copyright = '2024, Michael Turnbull'
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
        'sphinx.ext.coverage',
        'sphinxcontrib.plantuml',
        'sphinx_copybutton',
        'myst_parser',
        ]

templates_path = ['_templates']
exclude_patterns = ['_auto', '_build', 'Thumbs.db', '.DS_Store', 'README.md']

source_suffix = {
        '.rst': 'restructuredtext',
        '.md': 'markdown',
        }

rst_prolog = """
.. role:: python(code)
   :language: python
.. role:: py(code)
   :language: python
"""

# -- Options for InterSphinx -------------------------------------------------

intersphinx_mapping = {
        'python': ('https://docs.python.org/3', None),
        'pyvis': ('https://pyvis.readthedocs.io/en/latest', None),
        }
intersphinx_timeout = 10  # seconds

# -- Options for autodoc / autosummary ---------------------------------------

# may be "both", "signature", "description", or "none"
autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"
autodoc_typehints_format = "short"
autosummary_generate = True

# -- Options for ToDo ext ----------------------------------------------------

todo_include_todos = True

# -- Options for MyST Markdown Parser ----------------------------------------

myst_enable_extensions = [
        'tasklist',
        ]
myst_enable_checkboxes = True

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

warns = []

if eg_version.VERSION_MAJOR == 0:
    warns.append(
            "<b style=\"color:red;\">edgegraph is in unstable version " \
            f"{version}, and may change at any time!</b>")
if git.branchname() != "master" and not git.is_clean():
    warns.append(
            "<b style=\"color:yellow;\">this documentation was built on" \
            f" branch {git.branchname()}, and in an unclean git state!</b>")
elif git.branchname() != "master":
    warns.append(
            "<b style=\"color:yellow;\">this documentation was built on" \
            f" branch {git.branchname()}!</b>")
elif not git.is_clean():
    warns.append(
            "<b style=\"color:yellow;\">this documentation was built from " \
            "an unclean git repository!</b>")

html_theme_options["announcement"] = "<br>".join(warns)

# -- Options for LaTeX PDF output --------------------------------------------
# https://www.sphinx-doc.org/en/master/latex.html

latex_elements = {
        # make the index one column wide instead of two
        'printindex': r"\def\twocolumn[#1]{#1}\printindex",
        }

# show all urls / hyperlinks in footnotes (useful for printed copies)
latex_show_urls = 'footnote'
# same for page references
latex_show_pagerefs = True

# -- Options for coverage analysis -------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/coverage.html

# ensure that reports are written to the report file
# (_build/coverage/python.txt), and not printed to stdout
coverage_statistics_to_report = True
coverage_statistics_to_stdout = False

# these reports are also parsed (though, rather dumb-ly) during github actions,
# so ensure they're formatted like we expect
coverage_show_missing_items = False
coverage_write_headline = False

