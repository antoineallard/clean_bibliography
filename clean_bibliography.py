"""
Script extracting the bibliography's entries with a specific tag in Zotero.

Author: Antoine Allard (antoineallard.info)
"""
import json
import pandas
import bibtexparser
# import sys
# import os

class bibliography:

    # fields_to_keep = {
    #     'article': ['author', 'doi', 'journal', 'pages', 'title', 'url', 'volume', 'year', 'eprinttype', 'eprint', 'archiveprefix'],
    #     'book': ['author', 'doi', 'edition', 'editor', 'isbn', 'publisher', 'series', 'title', 'url', 'year', 'eprinttype', 'eprint', 'archiveprefix']
    #   }


    def __init__(self, source_bib_filename, abbrev_journal_names='abbreviations.csv', fields_to_keep='fields_to_keep.json'):

        self.source_bib_filename = source_bib_filename
        self.abbrev_journal_names = pandas.read_csv(abbrev_journal_names, comment='#', sep='[ \s]{2,}', engine='python').set_index('Complete Name')['Abbreviated Name'].to_dict()
        self.source_bib_database = bibtexparser.bparser.BibTexParser(common_strings=True).parse_file(open(source_bib_filename))
        self.fields_to_keep = json.load(open(fields_to_keep, 'r'))


    def clean_entry(self, entry, keep_keywords):

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
                        print('{}: field {} is not empty'.format(entry['ID'], field))
                        entry.pop(field, None)

            # for field in self.fields_to_keep[entry_type]:
            #     if field not in entry:
            #         if field == 'url':
            #             if 'doi' not in entry:
            #                 print('Entry {} is missing field {}.'.format(entry['ID'], field))
            #         elif field == 'doi':
            #             if 'url' not in entry:
            #                 print('Entry {} is missing field {}.'.format(entry['ID'], field))
            #         else:
            #             print('Entry {} is missing field {}.'.format(entry['ID'], field))

        # if 'keywords' in entry:
        #     entry['keywords'] = entry['keywords'].replace('{\_}', '_')
        #     entry['keywords'] = entry['keywords'].replace('\\_', '_')
        #     entry['keywords'] = entry['keywords'].replace(', ', ',')

        if 'title' in entry:
            entry['title'] = entry['title'].replace('{\{}', '{')
            entry['title'] = entry['title'].replace('{\}}', '}')

        if 'doi' in entry:
            entry.pop('url', None)

        if entry_type == 'article':
            if 'journal' in entry:
                if entry['journal'] == 'arXiv':
                    if 'eprint' in entry:
                        entry.pop('journal', None)
                        entry.pop('pages', None)

        # if len(entry['ID'].split('_')) == 3:
        #     entry['ID'] = ''.join([entry['ID'].split('_')[i] for i in [0, 2, 1]])


    def abbreviate_publication_name(self, entry):

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
                        print('No abbreviation provided for journal: {}'.format(journal_name))


    def extract_entries_with_given_keyword(self, tags_to_keep, target_bib_filename, keep_keywords=False):

        entries_to_keep = []
        for entry in self.source_bib_database.entries:
            if 'keywords' in entry:

                list_of_tags = entry['keywords']
                list_of_tags = list_of_tags.replace('{\_}', '_')
                list_of_tags = list_of_tags.replace('\\', '')
                list_of_tags = list_of_tags.replace(', ', ',')
                list_of_tags = list_of_tags.split(',')

                if any(tag in tags_to_keep for tag in list_of_tags):
                    self.clean_entry(entry, keep_keywords)
                    self.abbreviate_publication_name(entry)
                    entries_to_keep.append(entry)

        target_bib_database = bibtexparser.bibdatabase.BibDatabase()
        target_bib_database.entries = entries_to_keep
        bibtexparser.dump(target_bib_database, open(target_bib_filename, 'w'))


    def clean_entries(self, target_bib_filename, keep_keywords=False):

        entries_to_keep = []
        for entry in self.source_bib_database.entries:

            self.clean_entry(entry, keep_keywords)
            self.abbreviate_publication_name(entry)
            entries_to_keep.append(entry)

        target_bib_database = bibtexparser.bibdatabase.BibDatabase()
        target_bib_database.entries = entries_to_keep
        bibtexparser.dump(target_bib_database, open(target_bib_filename, 'w'))



def main():

    # if os.path.basename(os.getcwd()) != "clean_bibliography":
    #     os.chdir("clean_bibliography")


    # # tags_to_keep = ['biblio_phy7053']
    # # target_bib_filename = '/Users/antoine/Dropbox/backup/Documents/Enseignement/TheorieSystemesReseauxComplexes/2021/biblio/references.bib'
    # # keep_keywords = True

    # # tags_to_keep = ['bibl_directedS1', 'network_geometry', 'textbook']
    # # target_bib_filename = '/Users/antoine/Dropbox/dossiers_partages/directedS1/paper/references.bib'
    # # keep_keywords = False

    # tags_to_keep = ['network_geometry']
    # target_bib_filename = '../network_geometry/references.bib'
    # keep_keywords = True


    # bib = bibliography(source_bib_filename='../zotero/DynamicaLab.bib')
    # bib.extract_entries_with_given_keyword(tags_to_keep, target_bib_filename, keep_keywords)

    target_bib_filename = 'references.bib'
    keep_keywords = True
    source_bib_filename = 'references.bib'
    bib = bibliography(source_bib_filename)
    bib.clean_entries(target_bib_filename, keep_keywords)


if __name__ == "__main__":
    main()
