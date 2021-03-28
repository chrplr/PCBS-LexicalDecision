""" Select low and high frequency nouns and verbs from Lexique382.txt """

import pandas as pd

LEXIQUE_URL = 'http://www.lexique.org/databases/Lexique383/Lexique383.tsv'

SUBSET_SIZE = 20  # how many items in each category ((hi,low)*(nouns,verb)) are  needed

MIN_N_LETTERS = 5
MAX_N_LETTERS = 8

HIGH_FREQUENCY = 50
LOW_FREQUENCY = 10
ABS_THR = 1.0  # Absolute minimal threshold

lexique = pd.read_csv(LEXIQUE_URL, sep='\t')

# extract the relevant columns
lex = lexique[['ortho', 'cgram', 'nblettres', 'freqfilms2']]

# select potential items
medium_size_words = lex.loc[(lex.nblettres >= MIN_N_LETTERS) & (lex.nblettres <= MAX_N_LETTERS)]

noms = medium_size_words.loc[medium_size_words.cgram == 'NOM']
verbs = medium_size_words.loc[medium_size_words.cgram == 'VER']

noms_hi = noms.loc[noms.freqfilms2 > HIGH_FREQUENCY]
noms_low = noms.loc[(noms.freqfilms2 < LOW_FREQUENCY) & (noms.freqfilms2 > ABS_THR)]
verbs_hi = verbs.loc[verbs.freqfilms2 > HIGH_FREQUENCY]
verbs_low = verbs.loc[(verbs.freqfilms2 < LOW_FREQUENCY) & (verbs.freqfilms2 > ABS_THR)]


# extract samples among the potential items and save them in files
noms_hi.sample(SUBSET_SIZE).ortho.to_csv('nomhi.txt', index=False)
noms_low.sample(SUBSET_SIZE).ortho.to_csv('nomlo.txt', index=False)
verbs_hi.sample(SUBSET_SIZE).ortho.to_csv('verhi.txt', index=False)
verbs_hi.sample(SUBSET_SIZE).ortho.to_csv('verlo.txt', index=False)
