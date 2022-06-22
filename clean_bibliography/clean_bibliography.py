"""
Class and methods to extract the entries with a specific tag from an original bib file and to save the cleaned entries in another bib file.

Author: Antoine Allard (antoineallard.info)
"""
import sys
import json
import pandas
import pathlib
import bibtexparser


class Bibliography:


    def __init__(self, source_bib_filename):

        path = str(pathlib.Path(__file__).parent.resolve())

        abbrev_journal_names = '{}/config/abbreviations.txt'.format(path)
        self._abbrev_journal_names = pandas.read_csv(abbrev_journal_names, comment='#', sep='[ \s]{2,}', engine='python').set_index('Complete Name')['Abbreviated Name'].to_dict()

        fields_to_keep = '{}/config/fields_to_keep.json'.format(path)
        self._fields_to_keep = json.load(open(fields_to_keep, 'r'))

        minimal_fields = '{}/config/minimal_fields.json'.format(path)
        self._minimal_fields = json.load(open(minimal_fields, 'r'))

        self._missing_entry_types = []

        self._source_bib_filename = source_bib_filename
        self._load_source_bib_database()

        self._target_bib_database = bibtexparser.bibdatabase.BibDatabase()


    def clean_and_filter_entries(self, tags_to_keep=None, keep_keywords=False, warn_if_nonempty=False, warn_if_missing_fields=True, verbose=True):

        entries_to_keep = []
        for entry in self._source_bib_database.entries:
            if (tags_to_keep is None) or (self._has_at_least_one_keyword(entry, tags_to_keep)):
                self._clean_entry(entry, keep_keywords, warn_if_nonempty, warn_if_missing_fields, verbose)
                entries_to_keep.append(entry)

        self._target_bib_database.entries = entries_to_keep

        if verbose:
            self._display_missing_entry_types()


    def write_cleaned_and_filtered_entries_to_file(self, target_bib_filename=None, verbose=True):

        if target_bib_filename is None:
            path = pathlib.Path(self._source_bib_filename)
            path = path.with_name(path.stem + '_cleaned' + path.suffix)
            target_bib_filename = str(path)

        with open(target_bib_filename, 'w') as f:
            bibtexparser.dump(self._target_bib_database, f)
            if verbose:
                print('The cleaned bibliography can be found in {}'.format(target_bib_filename))


    def _abbreviate_publication_name(self, entry, verbose):

        entry_type = entry['ENTRYTYPE']
        if 'journal' not in entry:
            if 'eprint' not in entry:
                if verbose:
                    print('Entry {} does not have a journal.'.format(entry['ID']))
        else:
            journal_name = entry['journal'].replace('\&', '&')
            if journal_name in self._abbrev_journal_names:
                entry['journal'] = self._abbrev_journal_names[journal_name]
            else:
                if journal_name not in self._abbrev_journal_names.values():
                    if verbose:
                        print('No abbreviation provided for journal: {}. Please check the name of the journal or add the abbreviation to config/abbreviations.txt'.format(journal_name))


    def _check_for_missing_fields(self, entry):

        entry_type = entry['ENTRYTYPE']

        if entry_type == 'article':
            if 'journal' in entry:
                if entry['journal'] == 'arXiv':
                    entry_type = 'preprint'

        if entry_type not in self._minimal_fields:
            if entry_type not in self._missing_entry_types:
                self._missing_entry_types.append(entry_type)
        else:
            fields_in_entry = list(entry.keys())
            for field in self._minimal_fields[entry_type]:
                if field not in fields_in_entry:
                    if field == 'doi':
                        if 'url' not in fields_in_entry:
                            print('{}: both doi and url fields are empty (at least one should be given)'.format(entry['ID']))
                    else:
                        if (entry_type == 'preprint') and (field in ['volume', 'pages']):
                            continue
                        if (entry_type == 'book') and ('editor' in fields_in_entry):
                            continue
                        print('{}: field {} is empty'.format(entry['ID'], field))


    def _clean_entry(self, entry, keep_keywords, warn_if_nonempty, warn_if_missing_fields, verbose):

        entry_type = entry['ENTRYTYPE']

        if entry_type in ['article']:
            self._abbreviate_publication_name(entry, verbose)

        if entry_type not in self._fields_to_keep:
            if entry_type not in self._missing_entry_types:
                self._missing_entry_types.append(entry_type)

        else:
            entry.pop('abstract', None)
            entry.pop('annote', None)
            if keep_keywords == False:
                entry.pop('keywords', None)
            entry.pop('mendeley-tags', None)

            fields_in_entry = list(entry.keys())
            for field in fields_in_entry:
                if field not in ['ENTRYTYPE', 'ID', 'keywords']:
                    if field not in self._fields_to_keep[entry_type]:
                        if warn_if_nonempty and verbose:
                            print('{}: field {} is not empty'.format(entry['ID'], field))
                        entry.pop(field, None)

        if 'title' in entry:
            entry['title'] = entry['title'].replace('{\{}', '{')
            entry['title'] = entry['title'].replace('{\}}', '}')

        if 'doi' in entry:
            entry.pop('url', None)

        if warn_if_missing_fields and verbose:
            self._check_for_missing_fields(entry)

        if entry_type == 'article':
            if 'journal' in entry:
                if entry['journal'] == 'arXiv':
                    if 'eprint' in entry:
                        entry.pop('journal', None)
                        entry.pop('pages', None)


    def _display_missing_entry_types(self):

        if len(self._missing_entry_types) > 0:
            print('Warning, the following entry types are missing from fields_to_keep.json and/or minimal_fields.json: {}. They have not been thoroughly checked.'.format(', '.join(self._missing_entry_types)))


    def _has_at_least_one_keyword(self, entry, tags_to_keep):

        if 'keywords' in entry:
            list_of_tags = entry['keywords']
            list_of_tags = list_of_tags.replace('{\_}', '_')
            list_of_tags = list_of_tags.replace('\\', '')
            list_of_tags = list_of_tags.replace(', ', ',')
            list_of_tags = list_of_tags.split(',')
            return any(tag in tags_to_keep for tag in list_of_tags)

        else:
            return False


    def _load_source_bib_database(self):

        try:
            with open(self._source_bib_filename) as f:
                self._source_bib_database = bibtexparser.bparser.BibTexParser(common_strings=True).parse_file(f)

        except OSError:
            print('Error, could not read file: {}'.format(self._source_bib_filename))
            sys.exit()
