These are two scripts I use to generate clean bib files.

- [clean_bibfile.py](clean_bibfile.py): Removes superfluous fields (which are not included in [fields_to_keep.json](fields_to_keep.json)) from a specified bib file and abbreviates the journal names, if applicable (see [abbreviations.csv](abbreviations.csv)).

- [extract_bibfile_with_given_tags.py](extract_bibfile_with_given_tags.py): Extracts the entries with a specific tag from an original bib file and saves the cleaned entries in another bib file. When applicable, journal names are abbreviated (see [abbreviations.csv](abbreviations.csv)).


#### Customization

The fields to keep are specified in [fields_to_keep.json](fields_to_keep.json). Note that all fields are kept for entry types not specified in [fields_to_keep.json](fields_to_keep.json).

The journal abbreviations are specified in [abbreviations.csv](abbreviations.csv). Note that journals for which no abbreviation is provided will trigger a warning message and the original journal name will be kept in the new bib file.
