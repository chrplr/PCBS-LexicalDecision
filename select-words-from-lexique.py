#! /usr/bin/env python
# Time-stamp: <2021-03-30 13:01:24 christophe@pallier.org>
""" Select items from Lexique382.txt """

import argparse
import pandas as pd

parser = argparse.ArgumentParser(
    description='Select item from the Lexique database')
parser.add_argument('-n', type=int, default=10, help='number of items to pick')
parser.add_argument('--min-letters', type=int, default=3)
parser.add_argument('--max-letters', type=int, default=8)
parser.add_argument('--min-freq', type=float, default=1.0)
parser.add_argument('--max-freq', type=float, default=10000.0)
parser.add_argument('--cgram', type=str, default='NOM')
parser.add_argument(
    '--database',
    type=str,
    default='http://www.lexique.org/databases/Lexique383/Lexique383.tsv')

args = parser.parse_args()

# read lexique and extract the relevant columns
lex = pd.read_csv(args.database, sep='\t')

# apply selection criteria
length_selection = lex.loc[(lex.nblettres >= args.min_letters)
                           & (lex.nblettres <= args.max_letters)]

cgram_selection = length_selection.loc[length_selection.cgram == args.cgram]

freq_selection = cgram_selection.loc[
    (cgram_selection.freqfilms2 >= args.min_freq)
    & (cgram_selection.freqfilms2 <= args.max_freq)]

final_selection = freq_selection.sample(args.n)  # randomly pick n items

for _, word in final_selection['ortho'].items():
    print(word)
