import sys, os

extensions = ['sphinx.ext.autodoc']

project = 'Six Sigma SPC'
copyright = '2023'
author = 'Junior Marte Garcia, Marcel van Velzen'

sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(1, os.path.abspath('../SPC'))

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'alabaster'
html_static_path = ['_static']
autoclass_content = 'both'
