Lexical Decision Experiment
===========================


The aim of this project was to create a psycholinguistics experiment implementing a lexical decision task in the visual modality. 

The experiment consists in a succession of trials in which a written stimulus is displayed on the screen and the participant must indicate, by pressing one of two response buttons, if this stimulus is a word or not. The response time is recorded. 

The word stimuli are nouns and verbs of varying lexical frequencies (frequencies of occurrence in the language) to allow us to assess the influences of these two factors (Category: noun vs. verb; Frequency: high vs. low) on the speed of word recognition.


<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Lexical Decision Experiment](#lexical-decision-experiment)
    - [Preparation of the stimuli](#preparation-of-the-stimuli)
        - [Words](#words)
        - [Pseudowords](#pseudowords)
    - [Experimental list](#experimental-list)
    - [Experiment](#experiment)
    - [CONCLUSION](#conclusion)

<!-- markdown-toc end -->


## Preparation of the stimuli

### Words

We obtained a list of French words from <http://lexique.org>, downloading <http://www.lexique.org/public/Lexique382.zip> and unzipping it. Our first step was to reduce the number of columns to make it easier to handle the database. 
To this end, we wrote the script `reduce-lexique.py`:


    # reduce-lexique.py
    """ Extracts some columns from Lexique382.txt """

    import pandas as pd

    a = pd.read_csv('Lexique382.txt', sep='\t')

    b = a[['1_ortho', '4_cgram', '15_nblettres', '9_freqfilms2']].rename(columns={
       '1_ortho': 'ortho',
       '4_cgram': 'categ',
       '15_nblettres': 'length',
       '9_freqfilms2':'freq'})

    b.to_csv('lexique382-reduced.txt', sep='\t', index=False)


Then, we selected 4 subsets of nouns and verbs, of length comprosed between 5 and 8, with the following script (`select-word-from-lexique.py`):


    import pandas as pd

    lex = pd.read_csv("lexique382-reduced.txt", sep='\t')

    subset = lex.loc[(lex.length >= 5) & (lex.length <=8)]

    noms = subset.loc[subset.categ == 'NOM']
    verbs = subset.loc[subset.categ == 'VER']

    noms_hi = noms.loc[noms.freq > 50.0]
    noms_low = noms.loc[(noms.freq < 10.0) & (noms.freq > 1.0)]

    verbs_hi = verbs.loc[verbs.freq > 50.0]
    verbs_low = verbs.loc[(verbs.freq < 10.0) & (verbs.freq > 1.0)]

    N = 20

    noms_hi.sample(N).ortho.to_csv('nomhi.txt', index=False)
    noms_low.sample(N).ortho.to_csv('nomlo.txt', index=False)
    verbs_hi.sample(N).ortho.to_csv('verhi.txt', index=False)
    verbs_hi.sample(N).ortho.to_csv('verlo.txt', index=False)


This yielded 4 lists in four files:

    nomhi.txt  nomlo.txt  verhi.txt  verlo.txt



### Pseudowords

Then, to create 80 pseudowords, we used the lexique toolbox pseudoword generator (<http://www.lexique.org/toolbox/toolbox.pub/index.php?page=non_mot>), feeding it with the words generated at the previous step.

We obtained 80 pseudowords, listed in the file `pseudomots.txt`

## Experimental list

Importing the files `nomhi.txt  nomlo.txt  verhi.txt  verlo.txt and pseudomots.txt` into Openoffice Calc, we created a csv file `stimuli.csv`, with 3 columns:


    $ head stimuli.csv
    Category,Frequency,Item
    NOUN,HIFREQ,ordres
    NOUN,HIFREQ,reste
    NOUN,HIFREQ,couteau
    NOUN,HIFREQ,poisson
    ...


## Experiment

The script [lexical_decision.py](lexical_decision.py) to run the experiment uses the module [expyriment](www.epxyriment.org).

First, a list of trials is created, one for each row of `stimuli.csv`. Each trial contains a single stimulus, which is a `TextLine` containing the letter string to be displayed.

The list is randomized with `random.shuffle`.

Then the experiment starts. After the presentation of the stimulus, the scritps waits for a response key press, and then saved all the relevant information.

The results are stored in `data/lexical_decision*.xpd` files, with on file per subject. The xpd file is a csv file which can be imported in Excel, R or Python with pandas.

~~~
subject_id,categ,freq,item,key,rt,ok
6,VERB,HIFREQ,savais,102,928,False
6,PSEUDO,NA,brontai,102,1070,True
6,NOUN,LOFREQ,florin,106,751,True
6,PSEUDO,NA,fetreme,102,683,True
6,PSEUDO,NA,chétinct,102,662,True
6,PSEUDO,NA,protemci,102,656,True
6,VERB,LOFREQ,protéger,106,554,True
6,PSEUDO,NA,chlourbe,102,628,True
6,PSEUDO,NA,ébirial,102,998,True
6,VERB,LOFREQ,laissez,106,753,True
~~~


## CONCLUSION

It was a lot of work and we did not have time to implement all the thing we wanted to, notably:

* we wanted to write a script to analyse the data files and create a statistical report
* to include a training phase with feedback before the actual experiment


