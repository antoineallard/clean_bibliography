"""
Script extracts the entries with a specific tag from an original bib file and saves the cleaned entries in another bib file.

Author: Antoine Allard (antoineallard.info)
"""

from clean_bibliography import Bibliography

bib = Bibliography(source_bib_filename='../bibfiles/DynamicaLab.bib')

bib.extract_entries_with_given_keyword(tags_to_keep=['bibl_drDohn'], target_bib_filename='references.bib', keep_keywords=True)
