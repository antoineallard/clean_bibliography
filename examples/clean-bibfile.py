"""
Script cleans the entries of a bib file.

Author: Antoine Allard (antoineallard.info)
"""

import subprocess

<<<<<<< Updated upstream
source_bibfile = 'references.bib'

=======
source_bibfile = '../../references.bib'
>>>>>>> Stashed changes
cmd = ['python', '../cleanbib.py', source_bibfile, '-o', source_bibfile]
subprocess.run(cmd)

source_bibfile = '../../mypubs.bib'
cmd = ['python', '../cleanbib.py', source_bibfile, '-o', source_bibfile]
subprocess.run(cmd)

source_bibfile = '../../unpublished.bib'
cmd = ['python', '../cleanbib.py', source_bibfile, '-o', source_bibfile]
subprocess.run(cmd)

# source_bibfile = '../../low-rank.bib'
# cmd = ['python', '../cleanbib.py', source_bibfile, '-o', source_bibfile]
# subprocess.run(cmd)