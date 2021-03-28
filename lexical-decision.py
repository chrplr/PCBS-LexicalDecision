#! /usr/bin/env python
# Time-stamp: <2021-03-28 22:20:14 christophe@pallier.org>

import random
import csv
from expyriment import design, control, stimuli, misc


WORD_RESP = misc.constants.K_j
NONWORD_RESP = misc.constants.K_f
MAX_RESP_TIME = 2500
ITI = 1500  # inter trial interval
BUZZER = 'wrong-answer.ogg'

def show_instructions():
    stimuli.TextScreen("Instructions",
                       """You will see a sequence of written stimuli.

                       After each stimulus, your task is to press the right key ('J') if you think it is an existing word, the left key ('F') otherwise. Place now your index fingers on the keys 'F' and 'J'.

                       Press the SPACE BAR to start.""").present()
    exp.keyboard.wait_char(' ')


exp = design.Experiment(name="Lexical Decision Task", text_size=40) 

control.initialize(exp)

## Load the stimuli
trials = []
with open('stimuli.csv', 'r') as f:
    r = csv.reader(f)
    next(r)  # skip header line
    for row in r:
        cat, freq, item = row[0], row[1], row[2]
        trial = design.Trial()
        trial.add_stimulus(stimuli.TextLine(item))
        trial.set_factor("Category", cat)
        trial.set_factor("Frequency", freq)
        trial.set_factor("Item", item)
        trials.append(trial)

random.shuffle(trials)

negative_feedback = stimuli.Audio(BUZZER)

exp.add_data_variable_names(['category','frequency','item','response_key', 'rt', 'is_correct'])


# Run the experiment
control.start(skip_ready=True)

show_instructions()

for t in trials:
    exp.screen.clear()
    exp.screen.update()

    exp.clock.wait(ITI - t.stimuli[0].preload())
    t.stimuli[0].present()

    button, rt = exp.keyboard.wait([WORD_RESP, NONWORD_RESP],
                                   duration=MAX_RESP_TIME)

    cat = t.get_factor("Category")
    freq = t.get_factor("Frequency")

    is_correct = ((button == WORD_RESP) and (cat != 'PSEUDO')) or \
                 ((button == NONWORD_RESP) and (cat == 'PSEUDO'))
    if not is_correct:
        negative_feedback.play()

    exp.data.add([cat, freq, t.get_factor("Item"), button, rt, is_correct])

control.end()
