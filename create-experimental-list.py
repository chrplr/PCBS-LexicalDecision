#! /usr/bin/env python
# Time-stamp: <2021-03-30 14:17:52 christophe@pallier.org>
""" merge the items files (words and pseudowords) in a single csv file (to stdout).

For example:

   python create-experimental-list.py > trials.csv

"""

import os.path as op
import pandas as pd

STIM_DIR = 'stimuli/'

print('Category,Frequency,Item')

with open(op.join(STIM_DIR, 'nomhi.txt'), 'rt') as f:
    for item in f.read().splitlines():
        print('NOUN,HIFREQ,', item)

with open(op.join(STIM_DIR, 'nomlo.txt'), 'rt') as f:
    for item in f.read().splitlines():
        print('NOUN,LOFREQ,', item)

with open(op.join(STIM_DIR, 'verhi.txt'), 'rt') as f:
    for item in f.read().splitlines():
        print('VERB,HIFREQ,', item)

with open(op.join(STIM_DIR, 'verhi.txt'), 'rt') as f:
    for item in f.read().splitlines():
        print('VERB,LOFREQ,', item)

with open(op.join(STIM_DIR, 'pseudomots.txt'), 'rt') as f:
    for item in f.read().splitlines():
        print('PSEUDO,NA,', item)
