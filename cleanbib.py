"""
Script allowing to use the package via the terminal.

Author: Antoine Allard (antoineallard.info)
"""

import argparse

from clean_bibliography import Bibliography


parser = argparse.ArgumentParser()
parser.add_argument('source_bibfile')
parser.add_argument('-k', '--keywords', default=False, action='store_true',            help='keeps the keywords')
parser.add_argument('-n', '--names',    default=False, action='store_true',            help='prints the pdf filename (no further action is performed after)')
parser.add_argument('-o', '--output',   default=None,                                  help='name of the file in which the cleaned bibtex will be written (if omitted, "_cleaned" will be appended to the source filename)')
parser.add_argument('-q', '--quiet',    default=False, action='store_true',            help='quiet mode')
parser.add_argument('-t', '--tags',     default=None,                       nargs='+', help='tags used to filter the entries that will be kept')

args = parser.parse_args()

bib = Bibliography(source_bib_filename=args.source_bibfile)


if args.names:
    bib.PrintPDFFilenames(verbose=(not args.quiet))

else:
    bib.CleanBibfile(tags_to_keep=args.tags,
                     target_bib_filename=args.output,
                     keep_keywords=args.keywords,
                     warn_if_nonempty=False,
                     warn_if_missing_fields=True,
                     verbose=(not args.quiet))
