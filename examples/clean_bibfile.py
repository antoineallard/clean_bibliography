"""
Script cleans the entries of a bib file.

Author: Antoine Allard (antoineallard.info)
"""

from clean_bibliography import Bibliography

bib = Bibliography(source_bib_filename='references.bib')

bib.clean_bibfile(target_bib_filename='references.bib', keep_keywords=False)
