"""
Script builds the filenames for pdf based on a bib file.

Author: Antoine Allard (antoineallard.info)
"""

from clean_bibliography import bibliography


source_bib_filename = 'references.bib'
bib = bibliography(source_bib_filename)

target_filename = 'references.bib'
bib.build_pdf_filenames(target_filename)
