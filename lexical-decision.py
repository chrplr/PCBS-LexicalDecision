#! /usr/bin/env python
# Time-stamp: <2019-11-14 13:45:35 christophe@pallier.org>

""" Lexical decision experiment.

The experiment consists in a series of trials. In each trial, a letter string stimulus is displayed a thte center of the screen. The participant must press a button as quickly as possible to indicate if it is word or not.
"""

import random
import csv
import expyriment


WORD_RESP = expyriment.misc.constants.K_j  # key for WORD response
NONWORD_RESP = expyriment.misc.constants.K_f  # key for NONWORD response
MAX_RESP_TIME = 2500   # deadline for response time (msec)
ITI = 1500  # Inter trial interval (in msec)

exp = expyriment.design.Experiment(name="Lexical Decision Task") 

## Set develop mode. Comment for real experiment
# expyriment.control.set_develop_mode(on=True)

expyriment.control.initialize(exp)


## Load the stimuli
trials = []
with open('stimuli.csv', encoding="utf-8") as f:
    r = csv.reader(f)
    next(r)  # skip header line
    for row in r:
        cat, freq, item = row[0], row[1], row[2]
        trial = expyriment.design.Trial()
        trial.add_stimulus(expyriment.stimuli.TextLine(item))
        trial.set_factor("Category", cat)
        trial.set_factor("Frequency", freq)
        print(cat, freq)
        trial.set_factor("Item", item)
        trials.append(trial)

random.shuffle(trials)

exp.add_data_variable_names(['categ', 'freq', 'item', 'key', 'rt', 'ok'])

## Run the experiment
expyriment.control.start()

expyriment.stimuli.TextScreen("Instructions", """You will see a series of written stimuli displayed at the center of the screen.

After each stimulus, your task is to press the right key ('J') if you think it is an existing word, the left key ('F') otherwise. Place now your index fingers on the keys 'F' and 'J'.

Press the spacebar when you are ready to start.""").present()

exp.keyboard.wait_char(' ')
exp.screen.clear()
exp.screen.update()

for t in trials:
    exp.clock.wait(ITI - t.stimuli[0].preload())
    t.stimuli[0].present()
    button, rt = exp.keyboard.wait([WORD_RESP, NONWORD_RESP],
                                   duration=MAX_RESP_TIME)
    exp.screen.clear()
    exp.screen.update()

    cat = t.get_factor("Category")
    ok = ((button == WORD_RESP) and (cat != 'PSEUDO')) or ((button == NONWORD_RESP) and (cat == 'PSEUDO'))
    exp.data.add([cat,
                  t.get_factor("Frequency"),
                  t.get_factor("Item"),
                  button,
                  rt,
                  ok])

expyriment.control.end()
