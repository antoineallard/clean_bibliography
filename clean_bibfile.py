"""
Script cleaning the entries of a bib file.

Author: Antoine Allard (antoineallard.info)
"""

from clean_bibliography import Bibliography


source_bib_filename = 'references.bib'
bib = Bibliography(source_bib_filename)

target_bib_filename = 'references.bib'
keep_keywords = True
bib.clean_entries(target_bib_filename, keep_keywords)
