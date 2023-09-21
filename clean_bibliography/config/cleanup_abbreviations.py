import pandas
import tabulate

df = pandas.read_csv('abbreviations.txt', comment='#', sep='[ \s]{2,}', engine='python')

df = df.iloc[df['Abbreviated Name'].str.lower().argsort()]

df.drop_duplicates(inplace=True)

with open('abbreviations.txt', 'w') as f:

    f.write('#\n')
    f.write('# Using the ISO-4 standard of journal abbreviations\n')
    f.write('#\n')
    content = tabulate.tabulate(df.values.tolist(), headers=['Abbreviated Name', 'Complete Name'], tablefmt='plain')
    f.write(content)