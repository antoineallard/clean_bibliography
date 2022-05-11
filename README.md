Three scripts are provided to generate clean bib files.

- [clean_bibfile.py](clean_bibfile.py): Removes superfluous fields (which are not included in [fields_to_keep.json]) from a specified bib file and abbreviates the journal names, if applicable (see [abbreviations.txt]).

- [extract_entries_with_given_keyword.py](extract_entries_with_given_keyword.py): Extracts the entries with a specific tag from an original bib file and saves the cleaned entries in another bib file. When applicable, journal names are abbreviated (see [abbreviations.txt]).

- [build_pdf_filenames.py](build_pdf_filenames.py): Writes the filename for the pdf file for every article or book in a bib file into another text file. The convention is
  - Article: {abbreviated journal name}.{year}.{volume}.{first page}.{first author last name}.{title}.pdf
  - Book: {first author last name}.{year}.{title}.{edition, if specified}.pdf


#### Customization

The fields to keep are specified in [fields_to_keep.json]. Note that all fields are kept for entry types not specified in [fields_to_keep.json].

The journal abbreviations are specified in [abbreviations.txt]. Note that journals for which no abbreviation is provided will trigger a warning message and the original journal name will be kept in the new bib file.



[abbreviations.txt]:   config/abbreviations.txt
[fields_to_keep.json]: config/fields_to_keep.json
