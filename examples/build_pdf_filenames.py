"""
Script builds the filenames for pdf based on a bib file.

Author: Antoine Allard (antoineallard.info)
"""

import sys
import pathlib

path_root = pathlib.Path(__file__).parents[1]
sys.path.append(str(path_root))

from clean_bibliography import Bibliography


verbose = True

bib = Bibliography(source_bib_filename='references.bib')


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
    if 'eprinttype' in entry:
        if entry['eprinttype'] == 'arxiv':
            if 'eprint' in entry:
                page = entry['eprint'].split('.')[1]

    author = ''
    if 'author' in entry:
        author = entry['author']
    elif 'editor' in entry:
        author = entry['editor']
    author = author.split(',')[0]
    author = author.replace("{\\'a}",'a')
    author = author.replace("{\\'e}",'e')
    author = author.replace("{\\'i}",'i')
    # author = author.replace('{\\\"a}','a')
    author = author.replace('{\\c C}','C')
    author = author.replace('{\\v s}','s')
    author = author.replace('{\\~n}','n')
    author = author.replace('{','')
    author = author.replace('}','')
    author = author.replace('-','')
    author = author.replace("'",'')
    author = author.replace(' ','')
    author = author.replace("\\'",'')

    title = ''
    if 'title' in entry:
        title = entry['title']
        title = title.replace('\\textendash ','-')
        title = title.replace('{','')
        title = title.replace('}','')
        title = title.replace(' ','_')
        title = title.replace('-','')
        title = title.replace(':','')
        title = title.replace(',','')
        title = title.replace('(','')
        title = title.replace(')','')
        title = title.replace('\\"','')
        title = title.replace('`','')
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
        edition = edition.replace('First',   '1st')
        edition = edition.replace('Second',  '2nd')
        edition = edition.replace('Third',   '3rd')
        edition = edition.replace('Fourth',  '4th')
        edition = edition.replace('Fifth',   '5th')
        edition = edition.replace('Sixth',   '6th')
        edition = edition.replace('Seventh', '7th')
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
        print('.'.join(info) + '.pdf')

    if entry['ENTRYTYPE'] == 'book':
        info = []
        info.append(author)
        info.append(year)
        info.append(title)
        if edition != '':
            info.append(edition)
        print('.'.join(info) + '.pdf')
