# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

print('*' * 10)
print(os.path.abspath(".."))
sys.path.insert(0, os.path.abspath(".."))
os.environ['PATH'] += os.pathsep + 'C:/Program Files/Graphviz/bin'
graphviz_dot = 'C:/Program Files/Graphviz/bin/dot.exe'

project = 'NukeBridge'
copyright = '2024, Mahmoud Youssef'
author = 'Mahmoud Youssef'
release = '1.0.5'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.todo', 'sphinx.ext.viewcode', 'sphinx.ext.autodoc', 'sphinx.ext.inheritance_diagram',
              'sphinx.ext.graphviz',  # This should be listed to ensure Graphviz diagrams work
              ]

inheritance_graph_attrs = {
    'rankdir': 'TB',  # From top to bottom; change to 'LR' for left to right if preferred
    'size': '"6.0, 8.0"',  # Adjust as necessary to fit your diagram
    'fontsize': 14,
    'ratio': 'compress'  # Compress the graph layout
}
inheritance_node_attrs = dict(fontsize=16, height=0.75,
                              color='dodgerblue1', style='filled')
inheritance_edge_attrs = {
    'arrowsize': 0.8  # Smaller arrows; adjust as needed
}

# -- Options for autodoc extension -------------------------------------------
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
