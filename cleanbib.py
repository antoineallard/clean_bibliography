"""
Script allowing to use the module via the terminal.

Author: Antoine Allard (antoineallard.info)
"""

import argparse

from clean_bibliography import Bibliography


parser = argparse.ArgumentParser()
parser.add_argument('source_bibfile',   default='references.bib',           nargs='?')
parser.add_argument('-k', '--keywords', default=False, action='store_true',            help='keeps the keywords')
parser.add_argument('-e',               default=False, action='store_true',            help='warns if non essential fields are present in the original entries')
parser.add_argument('-m',               default=True,  action='store_false',           help='stops warning when essential fields are missing in the original entries')
parser.add_argument('-o', '--output',   default=None,                                  help='name of the file in which the cleaned bibtex will be written (if omitted, "_cleaned" will be appended to the source filename)')
parser.add_argument('-q', '--quiet',    default=False, action='store_true',            help='quiet mode')
parser.add_argument('-t', '--tags',     default=None,                       nargs='+', help='tags used to filter the entries that will be kept')

args = parser.parse_args()

bib = Bibliography(source_bib_filename=args.source_bibfile)

bib.clean_and_filter_entries(tags_to_keep=args.tags,
                             keep_keywords=args.keywords,
                             warn_if_nonempty=args.e,
                             warn_if_missing_fields=args.m,
                             verbose=(not args.quiet))

bib.write_cleaned_and_filtered_entries_to_file(target_bib_filename=args.output,
                                               verbose=(not args.quiet))