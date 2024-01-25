"""
Script cleans the entries of a bib file.

Author: Antoine Allard (antoineallard.info)
"""

import os
import pathlib
import subprocess

os.chdir(pathlib.Path(__file__).parents[0])

source_bibfile = 'references.bib'

cmd = ['python', '../cleanbib.py', source_bibfile, '-o', source_bibfile]

subprocess.run(cmd)
