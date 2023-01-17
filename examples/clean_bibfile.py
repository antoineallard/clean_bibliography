"""
Script cleans the entries of a bib file.

Author: Antoine Allard (antoineallard.info)
"""

import subprocess

source_bibfile = 'references.bib'

cmd = ['python', '../cleanbib.py', source_bibfile, '-o', source_bibfile]

subprocess.run(cmd)
