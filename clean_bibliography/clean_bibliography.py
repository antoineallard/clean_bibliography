"""
Class and methods to extract the entries with a specific tag from an original bib file and to save the cleaned entries in another bib file.

Author: Antoine Allard (antoineallard.info)
"""
import json
import pandas
import bibtexparser


class Bibliography:


    def __init__(self, source_bib_filename, abbrev_journal_names='config/abbreviations.txt', fields_to_keep='config/fields_to_keep.json', minimal_fields='config/minimal_fields.json'):

        self.source_bib_filename = source_bib_filename
        self.abbrev_journal_names = pandas.read_csv(abbrev_journal_names, comment='#', sep='[ \s]{2,}', engine='python').set_index('Complete Name')['Abbreviated Name'].to_dict()
        self.source_bib_database = bibtexparser.bparser.BibTexParser(common_strings=True).parse_file(open(source_bib_filename))
        self.fields_to_keep = json.load(open(fields_to_keep, 'r'))
        self.minimal_fields = json.load(open(minimal_fields, 'r'))


    def extract_entries_with_given_keyword(self, tags_to_keep, target_bib_filename, keep_keywords=False, warn_if_nonempty=True, warn_if_missing_fields=True):

        entries_to_keep = []
        for entry in self.source_bib_database.entries:
            if 'keywords' in entry:

                list_of_tags = entry['keywords']
                list_of_tags = list_of_tags.replace('{\_}', '_')
                list_of_tags = list_of_tags.replace('\\', '')
                list_of_tags = list_of_tags.replace(', ', ',')
                list_of_tags = list_of_tags.split(',')

                if any(tag in tags_to_keep for tag in list_of_tags):
                    self._clean_entry(entry, keep_keywords, warn_if_nonempty, warn_if_missing_fields)
                    self._abbreviate_publication_name(entry)
                    entries_to_keep.append(entry)

        self._write_bib_to_file(entries_to_keep, target_bib_filename)


    def clean_bibfile(self, target_bib_filename, keep_keywords=False, warn_if_nonempty=False, warn_if_missing_fields=True):

        entries_to_keep = []
        for entry in self.source_bib_database.entries:

            self._clean_entry(entry, keep_keywords, warn_if_nonempty, warn_if_missing_fields)
            self._abbreviate_publication_name(entry)
            entries_to_keep.append(entry)

        self._write_bib_to_file(entries_to_keep, target_bib_filename)


    def build_pdf_filenames(self, target_filename):

        with open(target_filename, 'w') as file:

            eol = ''
            if len(self.source_bib_database.entries) > 1:
                eol = '\n'

            for entry in self.source_bib_database.entries:

                self._clean_entry(entry, keep_keywords=False, warn_if_nonempty=False, warn_if_missing_fields=False)
                self._abbreviate_publication_name(entry)

                journal = ''
                if 'journal' in entry:
                    journal = entry['journal']
                    journal = journal.replace('.', '')
                    journal = journal.replace(' ', '')
                    journal = journal.replace('/', '')
                elif 'eprinttype' in entry:
                    if entry['eprinttype'] == 'arxiv':
                        journal = 'arXiv'

                year = ''
                if 'year' in entry:
                    year = entry['year']

                volume = ''
                if 'volume' in entry:
                    volume = entry['volume'].split('-')[0]
                elif 'eprinttype' in entry:
                    if entry['eprinttype'] == 'arxiv':
                        if 'eprint' in entry:
                            volume = entry['eprint'].split('.')[0]

                page = ''
                if 'pages' in entry:
                    page = entry['pages']
                    page = page.split('-')[0]
                    page = page.replace('.','dot')
                    page = page.replace(':','dot')
                elif 'eprinttype' in entry:
                    if entry['eprinttype'] == 'arxiv':
                        if 'eprint' in entry:
                            page = entry['eprint'].split('.')[1]

                author = ''
                if 'author' in entry:
                    author = entry['author']
                elif 'editor' in entry:
                    author = entry['editor']
                author = author.split(',')[0]
                author = author.replace('{\\\"a}','a')
                author = author.replace('{\c C}','C')
                author = author.replace('{','')
                author = author.replace('}','')
                author = author.replace('-','')
                author = author.replace(' ','')
                author = author.replace("\\'",'')

                title = ''
                if 'title' in entry:
                    title = entry['title']
                    title = title.replace('{','')
                    title = title.replace('}','')
                    title = title.replace(' ','_')
                    title = title.replace('-','')
                    title = title.replace(':','')
                    title = title.replace(',','')
                    title = title.replace('(','')
                    title = title.replace(')','')
                    title = title.replace("'","")
                    title = title.replace('/','_')
                    title = title.replace('?','')
                    title = title.replace('!','')
                    title = title.replace('.','')
                    title = title.replace('\\textsubscript','')
                    title = title.capitalize()

                edition = ''
                if 'edition' in entry:
                    edition = entry['edition']
                    edition = edition.replace('First', '1st')
                    edition = edition.replace('Second', '2nd')
                    edition = edition.replace('Third', '3rd')
                    edition = edition.replace('Fourth', '4th')
                    edition = edition.replace(' ', '')
                    edition = edition.replace('edition', '')

                if entry['ENTRYTYPE'] == 'article':
                    info = []
                    info.append(journal)
                    info.append(year)
                    info.append(volume)
                    info.append(page)
                    if author != '':
                        info.append(author)
                    info.append(title)
                    file.write('.'.join(info) + '.pdf' + eol)

                if entry['ENTRYTYPE'] == 'book':
                    info = []
                    info.append(author)
                    info.append(year)
                    info.append(title)
                    if edition != '':
                        info.append(edition)
                    file.write('.'.join(info) + '.pdf' + eol)


    def _abbreviate_publication_name(self, entry):

        entry_type = entry['ENTRYTYPE']
        if entry_type in ['article']:
            if 'journal' not in entry:
                if 'eprint' not in entry:
                    print('Entry {} does not have a journal.'.format(entry['ID']))
            else:
                journal_name = entry['journal'].replace('\&', '&')
                if journal_name in self.abbrev_journal_names:
                    entry['journal'] = self.abbrev_journal_names[journal_name]
                else:
                    if journal_name not in self.abbrev_journal_names.values():
                        print('No abbreviation provided for journal: {}. Please check the name of the journal or add the abbreviation to config/abbreviations.txt'.format(journal_name))


    def _check_for_missing_fields(self, entry):

        entry_type = entry['ENTRYTYPE']

        if entry_type == 'article':
            if 'journal' in entry:
                if entry['journal'] == 'arXiv':
                    entry_type = 'preprint'

        if entry_type not in self.fields_to_keep:
            print('Minimal fields not specified for entry type: {}'.format(entry_type))
        else:
            fields_in_entry = list(entry.keys())
            for field in self.minimal_fields[entry_type]:
                if field not in fields_in_entry:
                    if field == 'doi':
                        if 'url' not in fields_in_entry:
                            print('{}: both doi and url fields are empty (at least one should be given)'.format(entry['ID']))
                    else:
                        if (entry_type == 'preprint') and (field in ['volume', 'pages']):
                            continue
                        print('{}: field {} is empty'.format(entry['ID'], field))


    def _clean_entry(self, entry, keep_keywords, warn_if_nonempty, warn_if_missing_fields):

        entry_type = entry['ENTRYTYPE']
        if entry_type not in self.fields_to_keep:
            print('Fields to keep not specified for entry type: {}'.format(entry_type))
        else:
            entry.pop('abstract', None)
            entry.pop('annote', None)
            if keep_keywords == False:
                entry.pop('keywords', None)
            entry.pop('mendeley-tags', None)
            fields_in_entry = list(entry.keys())
            for field in fields_in_entry:
                if field not in ['ENTRYTYPE', 'ID', 'keywords']:
                    if field not in self.fields_to_keep[entry_type]:
                        if warn_if_nonempty:
                            print('{}: field {} is not empty'.format(entry['ID'], field))
                        entry.pop(field, None)

        if 'title' in entry:
            entry['title'] = entry['title'].replace('{\{}', '{')
            entry['title'] = entry['title'].replace('{\}}', '}')

        if 'doi' in entry:
            entry.pop('url', None)

        if warn_if_missing_fields:
            self._check_for_missing_fields(entry)

        if entry_type == 'article':
            if 'journal' in entry:
                if entry['journal'] == 'arXiv':
                    if 'eprint' in entry:
                        entry.pop('journal', None)
                        entry.pop('pages', None)


    def _write_bib_to_file(self, entries_to_keep, target_bib_filename):

        target_bib_database = bibtexparser.bibdatabase.BibDatabase()
        target_bib_database.entries = entries_to_keep
        with open(target_bib_filename, 'w') as f:
            bibtexparser.dump(target_bib_database, f)
