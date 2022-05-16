## Clean bibliography

This modules provides a set of functions to clean and check bibfiles to their use in publications.


### Examples

The functionalities of the module are illustrated via the following scripts:

- [clean_bibfile.py](examples/clean_bibfile.py): Removes superfluous fields (which are not included in [fields_to_keep.json]) from a specified bib file and abbreviates the journal names, if applicable (see [abbreviations.txt]).

- [extract_entries_with_given_keyword.py](examples/extract_entries_with_given_keyword.py): Extracts the entries with a specific tag from an original bib file and saves the cleaned entries in another bib file. When applicable, journal names are abbreviated (see [abbreviations.txt]).

- [build_pdf_filenames.py](examples/build_pdf_filenames.py): Writes the filename for the pdf file for every article or book in a bib file into another text file. The convention is
  - Article: {abbreviated journal name}.{year}.{volume}.{first page}.{first author last name}.{title}.pdf
  - Book: {first author last name}.{year}.{title}.{edition, if specified}.pdf


### Command-line tool

The module's functionalities can be accessed through a command-line interface provided by [bibclean.py](bibclean.py).
```bash
# Cleans the entries in original.bib and writes them in cleaned.bib
python bibclean.py original.bib -o cleaned.bib

# Cleans the entries in original.bib with tag1 and/or tag2 as keywords and writes them in cleaned.bib
python bibclean.py original.bib -t tag1 tag2 -o cleaned.bib
```
Further details can be found by executing
```bash
python bibclean.py --help
```


### Customization

The fields to keep are specified in [fields_to_keep.json]. Note that all fields are kept for entry types not specified in [fields_to_keep.json].

The fields that should minimally be present in any entries as specified in [minimal_fields.json].

The journal abbreviations are specified in [abbreviations.txt]. Note that journals for which no abbreviation is provided will trigger a warning message and the original journal name will be kept in the new bib file.



[abbreviations.txt]:   clean_bibliography/config/abbreviations.txt
[fields_to_keep.json]: clean_bibliography/config/fields_to_keep.json
[minimal_fields.json]: clean_bibliography/config/minimal_fields.json
