"""
Script builds the filenames for pdf based on a bib file.

Author: Antoine Allard (antoineallard.info)
"""

import sys
import pathlib

path_root = pathlib.Path(__file__).parents[1]
sys.path.append(str(path_root))

from clean_bibliography import Bibliography

bib = Bibliography(source_bib_filename='references.bib')

bib.PrintPDFFilenames(verbose=True)
