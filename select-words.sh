#! /bin/bash
# Time-stamp: <2021-03-30 13:04:32 christophe@pallier.org>

if [ ! -f "Lexique383.tsv" ]; then
    curl -O http://www.lexique.org/databases/Lexique383/Lexique383.tsv
fi

mkdir -p stimuli

python select-words-from-lexique.py -n 20 --cgram NOM --max-freq 5.0 --min-letters 5 --max-letters 8 --database Lexique383.tsv  > stimuli/nomlo.txt

python select-words-from-lexique.py -n 20 --cgram NOM --min-freq 100.0 --min-letters 5 --max-letters 8 --database Lexique383.tsv > stimuli/nomhi.txt

python select-words-from-lexique.py -n 20 --cgram VER --max-freq 5.0 --min-letters 5 --max-letters 8 --database Lexique383.tsv  > stimuli/verlo.txt

python select-words-from-lexique.py -n 20 --cgram VER --min-freq 100.0 --min-letters 5 --max-letters 8 --database Lexique383.tsv > stimuli/verhi.txt
