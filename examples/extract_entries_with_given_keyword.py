"""
Script extracts the entries with a specific tag from an original bib file and saves the cleaned entries in another bib file.

Author: Antoine Allard (antoineallard.info)
"""

import subprocess

source_bibfile = 'references.bib'
target_bibfile = 'references_cleaned.bib'

tags_to_keep = ['dimension_reduction', 'numerical_simulations']

cmd = ['python', '../cleanbib.py', source_bibfile, '-k', '-o', target_bibfile, '-t']
cmd.extend(tags_to_keep)

subprocess.run(cmd)
