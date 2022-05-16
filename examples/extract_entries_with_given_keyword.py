"""
Script extracts the entries with a specific tag from an original bib file and saves the cleaned entries in another bib file.

Author: Antoine Allard (antoineallard.info)
"""

import sys
import pathlib

path_root = pathlib.Path(__file__).parents[1]
sys.path.append(str(path_root))

from clean_bibliography import Bibliography

bib = Bibliography(source_bib_filename='../../bibfiles/DynamicaLab.bib')

bib.CleanBibfile(tags_to_keep=['bibl_drDohn'],
                 target_bib_filename='references.bib',
                 keep_keywords=True,
                 warn_if_nonempty=False,
                 warn_if_missing_fields=True,
                 verbose=True)
