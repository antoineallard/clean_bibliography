"""
Script cleans the entries of a bib file.

Author: Antoine Allard (antoineallard.info)
"""

import sys
import pathlib

path_root = pathlib.Path(__file__).parents[1]
sys.path.append(str(path_root))

from clean_bibliography import Bibliography

bib = Bibliography(source_bib_filename='references.bib')

bib.CleanBibfile(target_bib_filename='references.bib',
                 keep_keywords=False,
                 warn_if_nonempty=False,
                 warn_if_missing_fields=True,
                 verbose=True)
