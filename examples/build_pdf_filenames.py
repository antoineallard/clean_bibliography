"""
Script builds the filenames for pdf based on a bib file.

Author: Antoine Allard (antoineallard.info)
"""


import sys
import os
import pathlib
# import bibtexparser
# print(sys.version_info)

path_root = pathlib.Path(__file__).parents[1]
sys.path.append(str(path_root))
os.chdir(pathlib.Path(__file__).parents[0])

from clean_bibliography import Bibliography



def create_obsidian_note(title, doi, journal, year, filename):

    notes_path = '/Users/antoine/Library/Mobile Documents/iCloud~md~obsidian/Documents/science-notes/literature/literature-review'
    if not os.path.isfile(f"{notes_path}/{filename}.md"):

        title = title.replace("{", "").replace("}", "")

        with open(f"{notes_path}/{filename}.md", "w") as file:

            file_content = ('---\n'
                            'aliases:\n'
                           f'  - "{title}"\n'
                            'tags:\n'
                           f'title: "{title}"\n'
                            'authors:\n'
                           f'doi: https://doi.org/{doi}\n'
                           f'journal: "{journal}"\n'
                           f'year: "{year}"\n'
                           # f'bibentry: "{bibtexentry}"\n'
                            '---\n'
                            '##### Notes\n'
                            '\n'
                            '\n'
                           f'![[{filename}.pdf]]\n')

            file.write(file_content)
            print("Obsidian note created.")

    else:
        print("Obsidian note already exists.")


verbose = True

bib = Bibliography(source_bib_filename='./references.bib')


for entry in bib._source_bib_database.entries:

    entry_type = entry['ENTRYTYPE']
    if entry_type in ['article']:
        bib._abbreviate_publication_name(entry, verbose)

    journal = ''
    if 'journal' in entry:
        journal = entry['journal']
        journal = journal.replace('.', '')
        journal = journal.replace(' ', '')
        journal = journal.replace('/', '')
    elif 'archiveprefix' in entry:
        if entry['archiveprefix'] == 'arXiv':
            journal = 'arXiv'
        elif entry['archiveprefix'] == 'medRxiv':
            journal = 'medRxiv'
        elif entry['archiveprefix'] == 'bioRxiv':
            journal = 'bioRxiv'

    year = ''
    if 'year' in entry:
        year = entry['year']

    volume = ''
    if 'volume' in entry:
        volume = entry['volume'].split('-')[0]
    elif 'archiveprefix' in entry:
        if entry['archiveprefix'] == 'arXiv':
            if 'number' in entry:
                volume = entry['number'].split(':')[1].split('.')[0]
        elif entry['archiveprefix'] in ['medRxiv', 'bioRxiv']:
            if 'pages' in entry:
                volume = ''.join(entry['pages'].split('.')[1:3])

    page = ''
    if 'pages' in entry:
        page = entry['pages']
        page = page.split('-')[0]
        page = page.replace('.','dot')
        page = page.replace(':','dot')
    if 'archiveprefix' in entry:
        if entry['archiveprefix'] == 'arXiv':
            if 'eprint' in entry:
                page = entry['eprint'].split('.')[1]
        elif entry['archiveprefix'] in ['medRxiv', 'bioRxiv']:
            if 'pages' in entry:
                page = entry['pages'].split('.')[-1]

    author = ''
    if 'author' in entry:
        author = entry['author']
    elif 'editor' in entry:
        author = entry['editor']
    author = author.split(',')[0]
    author = author.replace("{\\'a}",'a')
    author = author.replace("{\\`a}",'a')
    author = author.replace("{\\`e}",'e')
    author = author.replace("{\\'c}",'c')
    author = author.replace("{\\'e}",'e')
    author = author.replace("{\\'i}",'i')
    author = author.replace("{\\l}",'l')
    author = author.replace("{\\'u}",'u')
    author = author.replace("{\\^o}",'o')
    author = author.replace("{\\`o}",'o')
    author = author.replace("{\\'o}",'o')
    author = author.replace('{\\"o}','o')
    author = author.replace('{\\"u}','u')
    # author = author.replace('{\\\"a}','a')
    author = author.replace('{\\c C}','C')
    author = author.replace('{\\c c}','c')
    author = author.replace('{\\v s}','s')
    author = author.replace('{\\v z}','z')
    author = author.replace('{\\~n}','n')
    author = author.replace("{\\'n}",'n')
    author = author.replace('{','')
    author = author.replace('}','')
    author = author.replace('-','')
    author = author.replace("'",'')
    author = author.replace(".",'')
    author = author.replace(' ','')
    author = author.replace("\\'",'')

    title = ''
    if 'title' in entry:
        title = entry['title']
        title = title.replace("\\'e",'e')
        title = title.replace("\\^e",'e')
        title = title.replace("\\`a",'a')
        title = title.replace("\\l ",'l')
        title = title.replace("\\.z",'z')
        title = title.replace('\\textendash ','-')
        title = title.replace('\\textendash','-')
        title = title.replace('\\textemdash','')
        title = title.replace('{','')
        title = title.replace('}','')
        title = title.replace('-','')
        title = title.replace(':','')
        title = title.replace(',','')
        title = title.replace('(','')
        title = title.replace(')','')
        title = title.replace('+','')
        title = title.replace('\\"','')
        # title = title.replace('\$','')
        title = title.replace('\\$','')
        title = title.replace('`','')
        title = title.replace("'","")
        title = title.replace('/','_')
        title = title.replace('?','')
        title = title.replace('!','')
        title = title.replace('~',' ')
        title = title.replace('.','')
        title = title.replace('\\textsubscript','')
        title = title.replace('$\\neq$','')
        title = title.replace('    ',' ')
        title = title.replace('   ',' ')
        title = title.replace('  ',' ')
        title = title.replace(' ','_')
        title = title.capitalize()

    edition = ''
    if 'edition' in entry:
        edition = entry['edition']
        edition = edition.replace('1',       '1st')
        edition = edition.replace('First',   '1st')
        edition = edition.replace('Second',  '2nd')
        edition = edition.replace('2',       '2nd')
        edition = edition.replace('Third',   '3rd')
        edition = edition.replace('3',       '3rd')
        edition = edition.replace('Fourth',  '4th')
        edition = edition.replace('Fifth',   '5th')
        edition = edition.replace('Sixth',   '6th')
        edition = edition.replace('Seventh', '7th')
        edition = edition.replace(' ', '')
        edition = edition.replace('edition', '')

    booktitle = ''
    if 'booktitle' in entry:
        booktitle = entry['booktitle']
        if booktitle in bib._abbrev_journal_names:
            booktitle = bib._abbrev_journal_names[booktitle]
        else:
            print('No abbreviation provided for conference: {}. Please check the name of the conference or add the abbreviation to config/abbreviations.txt'.format(booktitle))

    if entry_type == 'article':
        info = []
        info.append(journal)
        info.append(year)
        info.append(volume)
        info.append(page)
        if author != '':
            info.append(author)
        info.append(title)
        filename = '.'.join(info)
        print(filename)
        # bib._clean_entry(entry, keep_keywords=False, warn_if_nonempty=True, warn_if_missing_fields=True, verbose=False)
        # bibtex_entry = bibtexparser.dumps({"comments": None, ""})
        create_obsidian_note(entry['title'], entry['doi'], entry['journal'], year, filename)

    if entry_type == 'misc':
        if 'archiveprefix' in entry:
            if entry['archiveprefix'] in ['arXiv', 'medRxiv', 'bioRxiv']:
                info = []
                info.append(journal)
                info.append(year)
                info.append(volume)
                info.append(page)
                if author != '':
                    info.append(author)
                info.append(title)
                print('.'.join(info))

    if entry_type == 'book':
        info = []
        info.append(author)
        info.append(year)
        info.append(title)
        if edition != '':
            info.append(edition)
        print('.'.join(info))

    if entry_type == 'inproceedings':
        info = []
        info.append(booktitle)
        info.append(year)
        if volume != '':
            info.append(volume)
        info.append(page)
        if author != '':
            info.append(author)
        info.append(title)
        print('.'.join(info))

print("\n\n")


import subprocess

source_bibfile = 'references.bib'

cmd = ['python', '../cleanbib.py', source_bibfile, '-o', source_bibfile]

subprocess.run(cmd)